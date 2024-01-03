


import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
DEVICE_ADDRESS = 0x27  # replace with your device's address

# Here's a simple function to write some data to the device
def write_to_device(data):
    bus.write_byte(DEVICE_ADDRESS, data)
    time.sleep(0.1)

# Now let's write some example text
example_text = "VOLTS DISPlay, #1"
for char in example_text:
    write_to_device(ord(char))