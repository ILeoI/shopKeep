import platform

from application import Application

if platform.system() == "Windows":
    import drivers_win as drivers
else:
    import drivers_rpi as drivers

# TODO(ILeoI) update pages from db
# TODO(ILeoI) figure system for adding a new purchase (try to avoid genning pages for each person for each item,
#             maybe store some data in ListElement or Page and if set do something
#             flag for custom select


if __name__ == '__main__':
    app = Application()

    app.genGroceriesPage()

    display = drivers.Lcd()

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
        display.lcd_display_string(app.getCurrentPage().title, 1)

        text = app.getCurrentPage().getTextToDisplay()

        if text is not None:
            for i in range(0, len(text)):
                print(text[i])
                display.lcd_display_string(text[i], i+2)

        i = input("Input: ")

        if i == "X":
            display.lcd_clear()
            break
        elif i == "S":
            app.select()
        elif i == "B":
            app.back()
        elif i == "0":
            app.moveCursor(0)
        elif i == "1":
            app.moveCursor(1)
