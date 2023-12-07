import platform

if platform.system() == "Windows":
    WINDOWS = True
    import drivers_win as drivers
else:
    import drivers_rpi as drivers

if __name__ == '__main__':
    display = drivers.Lcd()

    while 1:
        try:
            display.lcd_display_string("Tom Stinks", 1)
            display.lcd_display_string("Tom Stinks", 2)
            display.lcd_display_string("Tom Stinks", 3)
            display.lcd_display_string("Tom Stinks", 4)
        except KeyboardInterrupt:
            display.lcd_clear()
            break

    pass

