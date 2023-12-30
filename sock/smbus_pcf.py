

import smbus
import time

# I2C bus address (adjust if necessary for your setup)
PCF8591_ADDRESS = 0x48

# Register addresses
PCF8591_ADC_REG = 0x00

# Create I2C bus object
bus = smbus.SMBus(1)  # Assuming I2C bus 1 is used

# Continuously read and print analog values
while True:
    data = bus.read_byte_data(PCF8591_ADDRESS, PCF8591_ADC_REG)
    data2 = bus.read_byte_data(0x49, PCF8591_ADC_REG)
    data3 = bus.read_byte_data(0x4A, PCF8591_ADC_REG)
    print("Analog value:", data)
    print("Analog value:", data2)
    print("Analog value:", data3)
    time.sleep(0.5)  # Delay between readings (adjust as needed)