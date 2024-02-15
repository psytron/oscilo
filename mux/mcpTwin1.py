import smbus
import time

# Create an SMBus instance
bus = smbus.SMBus(1)

# MCP23017 address
address = 0x20

# Configure MCP23017
bus.write_byte_data(address, 0x00, 0xFF)  # Set all pins on bank A to inputs
bus.write_byte_data(address, 0x01, 0xFF)  # Set all pins on bank B to inputs

# Read the state of the rotary encoder
def read_rotary_encoder():
    # Read the state of the CLK pin
    clk_state = bus.read_byte_data(address, 0x12) & 0x01  # Assuming CLK is connected to GPA0
    # Read the state of the DT pin
    dt_state = bus.read_byte_data(address, 0x12) & 0x02  # Assuming DT is connected to GPA1

    if clk_state == 0 and dt_state == 1:
        return 'clockwise'
    elif clk_state == 1 and dt_state == 0:
        return 'counter-clockwise'
    else:
        return 'idle'

# Main loop
while True:
    print(read_rotary_encoder())
    time.sleep(0.1)