
from threading import Event
from colorzero import Color
from gpiozero import RGBLED, Button
import smbus2 as smbus
import time

# Create I2C bus
bus = smbus.SMBus(1)

# MCP23017 I2C address
MCP23017 = 0x20

# MCP23017 Register addresses
IODIRA_REGISTER = 0x00  # IODIRA register (inputs/outputs)
GPIOA_REGISTER = 0x12  # GPIOA register (read inputs/write outputs)

# Set all pins as inputs by writing 0xFF to IODIRA register
bus.write_byte_data(MCP23017, IODIRA_REGISTER, 0xFF)

# Create a RotaryEncoder object
# The first parameter (16) is the pin number connected to the A or CLK pin of the rotary encoder
# The second parameter (20) is the pin number connected to the B or DT pin of the rotary encoder
rotor_clk = 16
rotor_dt = 20


done = Event()

rotor_steps = 0

def change_hue():
    global rotor_steps
    # Scale the rotor steps (-180..180) to 0..1
    rotor_clk_value = bus.read_byte_data(MCP23017, GPIOA_REGISTER + rotor_clk)
    rotor_dt_value = bus.read_byte_data(MCP23017, GPIOA_REGISTER + rotor_dt)
    if rotor_clk_value and rotor_dt_value:
        rotor_steps += 1
    elif not rotor_clk_value and not rotor_dt_value:
        rotor_steps -= 1
    print(rotor_steps)
    hue = (rotor_steps + 180) / 360

def show_color():
    print('Hue {led.color.hue.deg:.1f}° = {led.color.html}'.format(led=led))

 
while True:
    change_hue()
