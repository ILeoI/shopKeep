import sys
import time

from gpiozero import Button
from application import Application

WINDOWS = False
CONSOLE_MODE = True

if sys.argv.count("gpio") > 0:
    print("gpio input")
    CONSOLE_MODE = False

SELECT_BUTTON = 24
BACK_BUTTON = 25
DOWN_BUTTON = 23
UP_BUTTON = 18

if __name__ == '__main__':
    app = Application()

    app.genGroceriesPage()

    if not CONSOLE_MODE:
        selectButton = Button(SELECT_BUTTON)
        selectButton.when_released = app.select

        backButton = Button(BACK_BUTTON)
        backButton.when_released = app.back

        downButton = Button(DOWN_BUTTON)
        downButton.when_released = app.moveDown

        upButton = Button(UP_BUTTON)
        upButton.when_released = app.moveUp

    lastTime = time.time()

    while 1:
        currentTime = time.time()
        deltaTime = (currentTime - lastTime)

        app.update(deltaTime)

        try:
            if CONSOLE_MODE:
                i = input("Input: ")
                if i == "X":
                    app.clearLCD()
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
            print("")
            print("Stopped")
            break

        lastTime = currentTime
