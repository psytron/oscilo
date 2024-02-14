# PCF8591

import time
import numpy as np
import smbus

# Create an SMBus instance
bus = smbus.SMBus(1)

# PCF8591 address
address = 0x48

# Function to write data to DAC
def write_dac(data):
    bus.write_byte_data(address, 0x40, data)

# Generate a sine wave
x = np.linspace(0, 2 * np.pi, 256)
sine_wave = np.sin(x) * 127 + 128

while True:
    for value in sine_wave:
        write_dac(int(value))
        time.sleep(0.01)