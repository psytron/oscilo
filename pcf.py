import time
import board

import subprocess

import adafruit_pcf8591.pcf8591 as PCF
from adafruit_pcf8591.analog_in import AnalogIn
from adafruit_pcf8591.analog_out import AnalogOut

############# AnalogOut & AnalogIn Example ##########################
#
# This example shows how to use the included AnalogIn and AnalogOut
# classes to set the internal DAC to output a voltage and then measure
# it with the first ADC channel.
#
# Wiring:
# Connect the DAC output to the first ADC channel, in addition to the
# normal power and I2C connections
#
#####################################################################
i2c = board.I2C()  # uses board.SCL and board.SDA
#i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
pcf = PCF.PCF8591(i2c)

pcf_in_0 = AnalogIn(pcf, PCF.A0)
pcf_in_1 = AnalogIn(pcf, PCF.A1)
pcf_out = AnalogOut(pcf, PCF.OUT)

print( 'booting: ')
print( PCF.A0 , PCF.OUT , PCF )
while True:
    print( ' reference voltage: ', pcf_in_0.reference_voltage )
    pcf_out.value = 65535
    raw_value = pcf_in_1.value
    scaled_value = (raw_value / 65535) * pcf_in_0.reference_voltage

    print("pcf_in_1_scaled:", scaled_value )
    print( 'pcf_in_1_raw: ',pcf_in_1.value ) 

    print("Setting out to ", 32767)
    pcf_out.value = 32767
    raw_value = pcf_in_0.value
    scaled_value = (raw_value / 65535) * pcf_in_0.reference_voltage

    print("Pin 0: %0.2fV" % (scaled_value))
    #print("")
    #print("Setting out to ", 0)
    pcf_out.value = 0
    raw_value = pcf_in_0.value
    scaled_value = (raw_value / 65535) * pcf_in_0.reference_voltage

    #print("Pin 0: %0.2fV" % (scaled_value))
    
    
    
    print("\033c", end="")
