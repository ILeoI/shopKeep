import platform
import sys
import time

from gpiozero import Button
from application import Application

WINDOWS = False
CONSOLE_MODE = True

if sys.argv.count("gpio") > 0:
    print("gpio input")
    CONSOLE_MODE = False

if platform.system() == "Windows":
    WINDOWS = True
    import drivers_win as drivers
else:
    import drivers_rpi as drivers

SELECT_BUTTON = 24
BACK_BUTTON = 25
DOWN_BUTTON = 23
UP_BUTTON = 18

displayTitle = None
displayText = None

if __name__ == '__main__':
    app = Application()

    app.genGroceriesPage()

    display = drivers.Lcd()

    if not CONSOLE_MODE:
        selectButton = Button(SELECT_BUTTON)
        selectButton.when_released = app.select

        backButton = Button(BACK_BUTTON)
        backButton.when_released = app.back

        downButton = Button(DOWN_BUTTON)
        downButton.when_released = app.moveDown

        upButton = Button(UP_BUTTON)
        upButton.when_released = app.moveUp

    while 1:
        # app.printState()
        try:
            time.sleep(0.001)
            if app.shouldUpdate:
                app.shouldUpdate = False
                display.lcd_clear()

                display.lcd_display_string(app.getCurrentPage().title, 1)

                text = app.getCurrentPage().getTextToDisplay()

                if text is not None:
                    for i in range(0, len(text)):
                        display.lcd_display_string(text[i], i+2)

            if CONSOLE_MODE:
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

        except KeyboardInterrupt:
            print("stopped")
            display.lcd_clear()
            break
