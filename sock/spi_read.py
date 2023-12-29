


import spidev
import time

# SPI bus and device (adjust as needed)
bus = 0
device = 0

# Create SPI object
spi = spidev.SpiDev()
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