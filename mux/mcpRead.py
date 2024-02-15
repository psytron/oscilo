
import smbus2 as smbus
import time

bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1
address = 0x27  # replace with your MCP23017 device address

# MCP23017 Register addresses
IODIRA_REGISTER = 0x00  # IODIRA register (inputs/outputs)
GPIOA_REGISTER = 0x12  # GPIOA register (read inputs/write outputs)

# Set all pins as inputs by writing 0xFF to IODIRA register
bus.write_byte_data(address, IODIRA_REGISTER, 0xFF)

while True:
    # Read all 8 inputs from GPIOA
    inputs = bus.read_byte_data(address, GPIOA_REGISTER)
    print("Inputs: ", bin(inputs))

    time.sleep(1)  # delay between readings
