


import smbus2 as smbus
import time


bus = smbus.SMBus(1)

# PCF8591 I2C address
PCF8591 = 0x48

# Select the ADC channel. For example, channel 0
channel = 0

try:
    while True:
        # Write to the PCF8591 to select the channel
        bus.write_byte(PCF8591, channel)

        # Read the data from the PCF8591
        # The first read may be the old value, so read twice to get the latest value
        bus.read_byte(PCF8591)
        sensor_value = bus.read_byte(PCF8591)

        # Print the sensor value
        print("Sensor value: ", sensor_value)

        # Wait for a second before reading the sensor again
        time.sleep(1)

except KeyboardInterrupt:
    # Exit the script when CTRL+C is pressed
    print("Script exited")
