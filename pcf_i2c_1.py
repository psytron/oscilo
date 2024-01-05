





from smbus2 import SMBus
import time

bus = SMBus(1)  # 1 indicates /dev/i2c-1
address = 0x48  # replace with your device address
command_A0 = 0x40  # command for A0 pin
command_A1 = 0x41  # command for A1 pin

while True:
    # Read from A0
    bus.write_byte(address, command_A0)
    time.sleep(0.1)  # wait for ADC to complete
    value_A0 = bus.read_byte(address)
    print("A0 value:", value_A0)

    # Read from A1
    bus.write_byte(address, command_A1)
    time.sleep(0.1)  # wait for ADC to complete
    value_A1 = bus.read_byte(address)
    print("A1 value:", value_A1)

    time.sleep(1)  # delay between readings