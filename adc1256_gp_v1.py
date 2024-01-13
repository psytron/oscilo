

#  ADS1256 Data Acquisition board 
#  Enable SPI:
#  sudo raspi-config.
#  "Interfacing Options" -> "SPI" and enable it.

import RPi.GPIO as GPIO
# These libraries can be installed using pip:
# pip install ADS1256_definitions
# pip install pipyadc
from ADS1256_definitions import *
from pipyadc import ADS1256

 # Use the Raspberry Pi's GPIO Pins as SPI connection:
 # SPI (Serial Peripheral Interface) is a synchronous serial communication interface specification used for short distance communication.
 # It is primarily used in embedded systems. The SPI bus specifies four logic signals: SCK, MOSI, MISO, and CS.
 # SCK: Serial Clock (output from master)
 # MOSI: Master Output, Slave Input (output from master)
 # MISO: Master Input, Slave Output (output from slave)
 # CS: Chip Select (often active low, output from master)
 # Define the GPIO pins for the SPI interface on the Raspberry Pi
 # MOSI (Master Output, Slave Input): GPIO10
 # MISO (Master Input, Slave Output): GPIO9
 # SCK (Serial Clock): GPIO11
 # CS (Chip Select): GPIO8
 PINS = {"MOSI": 10, "MISO": 9, "SCK": 11, "CS": 8}

# Initialise the ADC using the default settings:
adc = ADS1256(pins=PINS)

# Gain and reference voltage.
adc.v_ref = 5

# Read data from all channels
data = adc.read_sequence(adc.CH_SEQUENCE)

# Print the raw data read from the ADC
print("Raw data from the ADC: ", data)
