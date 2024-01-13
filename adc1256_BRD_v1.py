



# Enable SPI:
#sudo raspi-config.
#Navigate to "Interfacing Options" -> "SPI" and enable it.
#Install libraries:
#sudo apt-get install python3-spidev python3-gpiozero



# HiLetgo ADS1256 board's pinout diagram and your Raspberry Pi's GPIO pinout.
# pins:
# ADS1256 CS (Chip Select) to a GPIO pin (e.g., GPIO8)
# ADS1256 DRDY (Data Ready) to another GPIO pin (e.g., GPIO17)
# ADS1256 CLK (Clock) to SPI SCLK (GPIO11)
# ADS1256 DIN (Data In) to SPI MOSI (GPIO10)
# ADS1256 DOUT (Data Out) to SPI MISO (GPIO9)
# VCC to 5V, GND to GND

import spidev
import gpiozero
import time

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # Adjust bus and device numbers if needed
spi.max_speed_hz = 1000000  # Set SPI clock speed

# GPIO setup
cs_pin = gpiozero.OutputDevice(8)  # Adjust GPIO pin if needed
drdy_pin = gpiozero.InputDevice(17)  # Adjust GPIO pin if needed

# ADS1256 commands (adjust as needed)
CMD_RESET = 0x06
CMD_START = 0x08
CMD_POWERDOWN = 0x02
CMD_RDATA = 0x10

# Register setup (adjust as needed)
REG_CONFIG1 = 0x00
REG_CONFIG2 = 0x01
REG_CONFIG3 = 0x02

# Configuration values (adjust as needed)
GAIN = 1  # Gain setting (1, 2, 4, or 8)
DR = 1000  # Data rate (SPS)

def init_ads1256():
    # Reset the ADS1256
    cs_pin.on()
    spi.writebytes([CMD_RESET])
    cs_pin.off()
    time.sleep(0.005)

    # Write configuration registers
    config_bytes = [
        (REG_CONFIG1, 0b10000000 | (GAIN - 1) << 4 | DR << 1),
        (REG_CONFIG2, 0x04),  # Internal reference
        (REG_CONFIG3, 0x00),  # Disable comparator
    ]
    for reg, value in config_bytes:
        cs_pin.on()
        spi.writebytes([CMD_WREG | reg, 0x00, value])
        cs_pin.off()

def read_single_channel(channel):
    # Start a single-channel conversion
    cs_pin.on()
    spi.writebytes([CMD_WREG | REG_MUX, 0x00, channel])
    spi.writebytes([CMD_START])
    cs_pin.off()

    # Wait for DRDY to go low
    while drdy_pin.is_active:
        pass

    # Read the data
    cs_pin.on()
    spi.writebytes([CMD_RDATA])
    data = spi.readbytes(3)
    cs_pin.off()

    # Convert the raw data to voltage
    value = (data[0] << 16) | (data[1] << 8) | data[2]
    voltage = value * 4.096 / (2 ** 23)  # Assuming 5V reference
    return voltage

# Example usage
init_ads1256()
voltage = read_single_channel(0)  # Read channel 0
print("Voltage")
