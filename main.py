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

    # Generate all the pages
    app.genAppPages()


    # Assigning functions to button presses
    if not CONSOLE_MODE:
        selectButton = Button(SELECT_BUTTON)
        selectButton.when_released = app.select

        backButton = Button(BACK_BUTTON)
        backButton.when_released = app.back

        downButton = Button(DOWN_BUTTON)
        downButton.when_released = app.moveDown

        upButton = Button(UP_BUTTON)
        upButton.when_released = app.moveUp

        app.doSleep = True

    lastTime = time.time()

    # App Update Loop
    while 1:
        currentTime = time.time()
        deltaTime = (currentTime - lastTime)

        try:
            app.update(deltaTime)

            if CONSOLE_MODE:
                app.printState(consoleMode=True)

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
            app.clearLCD()
            break

        lastTime = currentTime
