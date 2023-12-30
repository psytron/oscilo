


import spidev
import time

# SPI bus and device (adjust as needed)
bus = 0
device = 0



# Create SPI object
# Implicit Pin Configuration:
# spi = spidev.SpiDev() creates an SPI object that implicitly uses 
# the default SPI pins for the specified bus and device:
# Bus 0: MOSI = GPIO 10, MISO = GPIO 9, SCLK = GPIO 11
# Bus 1: MOSI = GPIO 19, MISO = GPIO 21, SCLK = GPIO 23
spi = spidev.SpiDev()
# spi.open(bus, device) opens the SPI bus and device, using those default pin assignments.
spi.open(bus, device)

# Set SPI mode and clock speed
spi.mode = 0  # Mode 0 (most common)
spi.max_speed_hz = 1000000  # Adjust clock speed as needed

try:
    while True:
        # Read a specified number of bytes (adjust as needed)
        data = spi.readbytes(3)  # Example: reading 3 bytes

        # Process the received data
        print(data)  # Example: print the data

        # Add any necessary processing or actions based on the data

        # Adjust the delay between readings as needed
        time.sleep(0.1)  # Example: wait 0.1 seconds

except KeyboardInterrupt:
    # Close the SPI connection on exit
    spi.close()