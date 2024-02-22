from threading import Event
from colorzero import Color
from gpiozero import RotaryEncoder, RGBLED, Button

# Create a RotaryEncoder object
# The first parameter (16) is the pin number connected to the A or CLK pin of the rotary encoder
# The second parameter (20) is the pin number connected to the B or DT pin of the rotary encoder
# The 'wrap' parameter set to True allows the rotary encoder to loop from its maximum value back to its minimum value and vice versa
# The 'max_steps' parameter (180) sets the maximum number of steps the rotary encoder can take in one direction
rotor = RotaryEncoder(16, 20, wrap=False, max_steps=1800)
rotor.steps = 0
led = RGBLED(22, 23, 24, active_high=False)
btn = Button(21, pull_up=False)
led.color = Color('#f00')
done = Event()

def change_hue():
    # Scale the rotor steps (-180..180) to 0..1
    print(  rotor.steps )
    hue = (rotor.steps + 180) / 360
    led.color = Color(h=hue, s=1, v=1)

def show_color():
    print('Hue {led.color.hue.deg:.1f}° = {led.color.html}'.format(led=led))

def stop_script():
    print('Exiting')
    done.set()


rotor.when_rotated = change_hue
btn.when_released = show_color  # Push the button to see the HTML code for the color
btn.when_held = stop_script     # Hold the button to exit
done.wait()