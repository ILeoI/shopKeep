from gpiozero import Button

button = Button(24)

button.wait_for_press()
print("pressed")
