import platform
import sys

from application import Application

WINDOWS = False
CONSOLE_MODE = True

if sys.argv.count("gpio") > 0:
    print("gpio input")
    CONSOLE_MODE = False

if platform.system() == "Windows" or WINDOWS:
    WINDOWS = True
    import drivers_win as drivers
    import RPiGPIO as GPIO
else:
    import drivers_rpi as drivers
    import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

button_pins = [17, 18, 22, 23]

if not CONSOLE_MODE:
    for pin in button_pins:
       GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
        else:
            try:
                channel = GPIO.wait_for_edge(button_pins, GPIO.RISING)
                pressed_button = button_pins.index(channel)
            except KeyboardInterrupt:
                pass
        
        display.lcd_clear()
