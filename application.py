from typing import List

import pymysql.cursors

from page import Page
from list_element import ListElement


class Application:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost",
            database="sharing",
            user="dbadmin",
            password="",
            cursorclass=pymysql.cursors.DictCursor
        )
        self.pages: List[Page] = []
        self.previousPages: List[int] = []
        self.currentPageIndex = 0

    def fetchResultFromDB(self, sql: str, *args):
        for arg in args:
            sql = sql.replace("%s", arg, 1)

        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    def runSQLOnDB(self, sql: str, *args):
        for arg in args:
            sql = sql.replace("%s", str(arg), 1)

        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    def addPage(self, page: Page):
        self.pages.append(page)

    def getCurrentPage(self):
        return self.pages[self.currentPageIndex]

    def moveCursor(self, direction):
        self.getCurrentPage().moveCursor(direction)

    def back(self):
        if len(self.previousPages) > 0:
            self.currentPageIndex = self.previousPages.pop()

    def select(self):
        currentListElement = self.getCurrentPage().getCurrentListElement()
        if currentListElement.selectable:
            if currentListElement.dataType == "link":
                link = currentListElement.data
                if link is not None:
                    for i in range(0, len(self.pages)):
                        page = self.pages[i]
                        if page.id == link:
                            page.currentElementIndex = 0
                            self.previousPages.append(self.currentPageIndex)
                            self.currentPageIndex = i
            if currentListElement.dataType == "add":
                (userID, groceryID) = currentListElement.data
                self.runSQLOnDB("INSERT INTO PurchaseHistory(userID, groceryID, purchaseDate) VALUES(%s, %s, now())",
                                userID, groceryID
                                )
                self.regenGroceryHistoryPage(str(groceryID))
                self.back()

    def regenGroceryHistoryPage(self, groceryID: str):
        historyPage = None

        for page in self.pages:
            if page.id == "history" + groceryID:
                historyPage = page

        if historyPage is None:
            print("history" + groceryID + " is none")
            return

        gID = historyPage.id.replace("history", "")

        results = self.fetchResultFromDB(
            "SELECT Users.name as buyer, purchaseDate "
            "FROM PurchaseHistory "
            "JOIN Users on PurchaseHistory.userID = Users.userID "
            "JOIN Groceries on PurchaseHistory.groceryID = Groceries.groceryID "
            "WHERE Groceries.groceryID = %s "
            "ORDER BY purchaseDate DESC "
            "LIMIT 5",
            gID
        )

        historyPage.elements.clear()

        for result in results:
            text = result["buyer"] + "        "[len(result["buyer"]):] + str(result["purchaseDate"])
            historyPage.addElement(ListElement(text))

    def genGroceryHistoryPage(self, groceryName: str, groceryID: str):
        page = Page(id="history" + groceryID, title=groceryName)
        gID = groceryID.replace("grocery", "")
        results = self.fetchResultFromDB(
            "SELECT Users.name as buyer, purchaseDate "
            "FROM PurchaseHistory "
            "JOIN Users on PurchaseHistory.userID = Users.userID "
            "JOIN Groceries on PurchaseHistory.groceryID = Groceries.groceryID "
            "WHERE Groceries.groceryID = %s "
            "ORDER BY purchaseDate DESC "
            "LIMIT 5",
            gID
        )

        for result in results:
            text = result["buyer"] + "        "[len(result["buyer"]):] + str(result["purchaseDate"])
            page.addElement(ListElement(text))

        self.pages.append(page)

    def genGroceryAddPage(self, groceryName: str, groceryID: str):
        page = Page(title=groceryName, id="add" + groceryID)

        results = self.fetchResultFromDB(
            "SELECT Users.name, Users.userID, Groceries.groceryID "
            "FROM Sharing "
            "JOIN Users on sharing.userID = users.userID "
            "JOIN Groceries on sharing.groceryID = groceries.groceryID "
            "WHERE Groceries.groceryID = %s",
            groceryID
        )

        for result in results:
            page.addElement(
                ListElement(result["name"],
                            selectable=True,
                            dataType="add",
                            data=(result["userID"], result["groceryID"])
                            )
            )

        self.pages.append(page)

    def genGroceryOptionPage(self, groceryName: str, groceryID: str):
        page = Page(title=groceryName, id="option" + groceryID)
        results = self.fetchResultFromDB(
            "SELECT count(*) as x, users.name "
            "FROM purchasehistory "
            "JOIN Users on purchasehistory.userID = users.userID "
            "WHERE purchasehistory.groceryID = %s "
            "GROUP BY purchasehistory.userID "
            "ORDER BY purchasehistory.purchaseDate",
            groceryID)

        if len(results) != 0:
            even = False
            minX = 0
            minIndex = -1

            for i in range(0, len(results)):
                if minIndex == -1:
                    minIndex = i
                    minX = results[i]["x"]

                if results[i]["x"] < minX:
                    minIndex = i
                    minX = results[i]["x"]

                if results[i]["x"] == minX:
                    even = True
                else:
                    even = False

            if even:
                page.addElement(ListElement("Next Buyer: " + results[0]["name"]))
            else:
                page.addElement(ListElement("Next Buyer: " + results[minIndex]["name"]))

        page.addElement(ListElement("Add", selectable=True, dataType="link", data="add" + groceryID))
        page.addElement(ListElement("History", selectable=True, dataType="link", data="history" + groceryID))

        self.pages.append(page)

    def genGroceriesPage(self):
        results = self.fetchResultFromDB("SELECT * FROM Groceries")

        groceryPage = Page(id="groceryList", title="Groceries")

        self.pages.append(groceryPage)

        for result in results:
            groceryName = result["name"]
            groceryID = str(result["groceryID"])

            self.genGroceryOptionPage(groceryName, groceryID)
            self.genGroceryHistoryPage(groceryName, groceryID)
            self.genGroceryAddPage(groceryName, groceryID)

            groceryPage.addElement(
                ListElement(displayText=groceryName, selectable=True, dataType="link", data="option" + groceryID)
            )

    def printState(self):
        print("currentPageIndex: " + str(self.currentPageIndex))
        print("prevPages: " + str(self.previousPages))
        for page in self.pages:
            print(page.title + ": " + str(len(page.elements)))
            print(page.id)
            for element in page.elements:
                print(element.displayText)
            print()
