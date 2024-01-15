


import spidev

# Create a SpiDev object
spi = spidev.SpiDev()

# Open the SPI device. The first parameter is the bus number and the second is the device number.
spi.open(0, 0)

# Set the SPI mode and speed
spi.mode = 0b01
spi.max_speed_hz = 20000

# Read 10 bytes of data
data = spi.readbytes(10)

# Don't forget to close the SPI device when you're done
spi.close()

