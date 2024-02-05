from typing import List, Dict

import platform
import sys
import time

import pymysql.cursors

from page import Page
from list_element import ListElement

if platform.system() == "Windows":
    WINDOWS = True
    import drivers_win as drivers
else:
    import drivers_rpi as drivers

LOG = False

if sys.argv.count("log") > 0:
    print("logging")
    LOG = True

TIME_STILL_SLEEP = 30.0

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
        self.shouldUpdate = True
        self.awake = True
        self.timeTillSleep = TIME_STILL_SLEEP
        self.display = drivers.Lcd()
        self.textToDisplay: Dict[str] = {}

    def update(self, deltaTime):
        if self.timeTillSleep > 0:
            self.timeTillSleep -= deltaTime
        else:
            if self.awake:
                self.toggleScreen()

        time.sleep(0.001)
        self.textToDisplay.clear()

        if self.shouldUpdate:
            self.shouldUpdate = False
            self.display.lcd_clear()

            self.display.lcd_display_string(self.getCurrentPage().title, 1)
            self.textToDisplay["Title"] = self.getCurrentPage().title

            text = self.getCurrentPage().getTextToDisplay()

            if text is not None:
                for i in range(0, len(text)):
                    self.textToDisplay["Line" + str(i)] = text[i]
                    self.display.lcd_display_string(text[i], i + 2)

        if LOG:
            self.printState()

    def clearLCD(self):
        self.display.lcd_clear()

    def toggleScreen(self):
        if self.awake:
            self.awake = False
            self.display.lcd_backlight(state=0)

        elif not self.awake:
            self.awake = True
            self.display.lcd_backlight(state=1)
            self.resetSleepTimer()

    def resetSleepTimer(self):
        print("reset sleep timer")
        self.timeTillSleep = TIME_STILL_SLEEP

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
        self.shouldUpdate = True

    def moveDown(self):
        if not self.awake:
            self.toggleScreen()

        self.moveCursor(1)
        self.shouldUpdate = True

    def moveUp(self):
        if not self.awake:
            self.toggleScreen()
            return

        self.resetSleepTimer()

        self.moveCursor(0)
        self.shouldUpdate = True

    def back(self):
        if not self.awake:
            self.toggleScreen()
            return

        self.resetSleepTimer()

        if len(self.previousPages) > 0:
            self.currentPageIndex = self.previousPages.pop()
            self.shouldUpdate = True

    def select(self):
        if not self.awake:
            self.toggleScreen()
            return

        self.resetSleepTimer()
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
                self.regenGroceryOptionPage(str(groceryID))

                self.back()
        self.shouldUpdate = True

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
            "ORDER BY purchaseDate DESC ",
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
            "JOIN Users on Sharing.userID = Users.userID "
            "JOIN Groceries on Sharing.groceryID = Groceries.groceryID "
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

    def regenGroceryOptionPage(self, groceryID: str):
        optionPage = None

        for page in self.pages:
            if page.id == "option" + groceryID:
                optionPage = page

        if optionPage is None:
            print("option" + groceryID + " is none")
            return

        optionPage.elements.clear()

        optionPage.addElement(ListElement("Next Buyer: " + self.findNextBuyer(groceryID)))

        optionPage.addElement(ListElement("Add", selectable=True, dataType="link", data="add" + groceryID))
        optionPage.addElement(ListElement("History", selectable=True, dataType="link", data="history" + groceryID))

    def genGroceryOptionPage(self, groceryName: str, groceryID: str):
        page = Page(title=groceryName, id="option" + groceryID)

        page.addElement(ListElement("Next Buyer: " + self.findNextBuyer(groceryID)))

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

    def findNextBuyer(self, groceryID: str):
        results = self.fetchResultFromDB(
            "SELECT Users.name, COUNT(PurchaseHistory.groceryID) AS purchaseCount, "
            "   MAX(PurchaseHistory.purchaseDate) as lastPurchaseDate "
            "FROM Sharing "
            "LEFT JOIN PurchaseHistory ON Sharing.userID = PurchaseHistory.userID "
            "   AND PurchaseHistory.groceryID = Sharing.groceryID "
            "JOIN Users on Sharing.userID = Users.userID "
            "WHERE Sharing.groceryID = %s "
            "GROUP BY Sharing.userID, Sharing.groceryID;",
            groceryID)

        next_buyer = min(results, key=lambda x: (x['purchaseCount'], x['lastPurchaseDate']))

        return next_buyer["name"]

    def printState(self):
        for i in self.textToDisplay:
            print(i + ": " + self.textToDisplay[i])

        if self.timeTillSleep != 0:
            print("TTS: " + str(self.timeTillSleep))
            print("Awake: " + str(self.awake))
