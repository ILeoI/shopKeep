import platform
import time

if platform.system() == "Windows":
    WINDOWS = True
    import drivers_win as drivers
else:
    import drivers_rpi as drivers

if __name__ == '__main__':
    display = drivers.Lcd()

    i = 0

    while 1:
        try:
            display.lcd_display_string("Tom Stinks", (i % 4) + 1)
            time.sleep(0.5)
            display.lcd_clear()
            i += 1
        except KeyboardInterrupt:
            display.lcd_clear()
            break

    pass

