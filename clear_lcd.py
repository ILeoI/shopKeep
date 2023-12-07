import platform

if platform.system() == "Windows":
    WINDOWS = True
    import drivers_win as drivers
else:
    import drivers_rpi as drivers

if __name__ == '__main__':
    display = drivers.Lcd()
    display.lcd_clear()