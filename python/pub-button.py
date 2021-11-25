import fourletterphat as flp
import signal
import buttonshim

# get temperature


# display temperature

while True:
    flp.clear()
    display = input('Voer bericht van 4 karakters in:\n')
    flp.print_str(display)
    flp.show()

## define buttons (1-start, 2-accept (=reset), 3-deny (=reset), 4-set max temp (up, down, accept, cancel)

print("""
Button SHIM: rainbow.py

Light up the LED a different colour of the rainbow with each button pressed.

Press Ctrl+C to exit.

""")
@buttonshim.on_press(buttonshim.BUTTON_A) #PURPLE
def button_a(button, pressed):

signal.pause()

## set max temperature

# set LED color based on temperature and max temperature

    buttonshim.set_pixel(0x00, 0xff, 0x00) #GREEN
    buttonshim.set_pixel(0xff, 0xff, 0x00) #YELLOW
    buttonshim.set_pixel(0xff, 0x00, 0x00) #RED

