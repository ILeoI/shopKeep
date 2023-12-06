from application import Application

# TODO(leo) update pages from db
# TODO(leo) figure system for adding a new purchase (try to avoid genning pages for each person for each item,
#           maybe store some data in ListElement or Page and if set do something
#           flag for custom select


if __name__ == '__main__':
    app = Application()

    app.genGroceriesPage()

    while 1:
        print()
        print()
        print()
        print()
        print()
        print()
        print()

        # app.printState()
        print()

        print(app.getCurrentPage().title)

        text = app.getCurrentPage().getTextToDisplay()

        if text is not None:
            for s in text:
                print(s)

        i = input("Input: ")

        if i == "X":
            break
        elif i == "S":
            app.select()
        elif i == "B":
            app.back()
        elif i == "0":
            app.moveCursor(0)
        elif i == "1":
            app.moveCursor(1)
