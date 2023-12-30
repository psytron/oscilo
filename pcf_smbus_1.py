import smbus
import time

# Define the I2C address for the PCF8591
pcf_address = 0x48  # This is the default address, adjust if necessary

# Create an smbus object
bus = smbus.SMBus(1)  # Use 0 for older Raspberry Pi boards

# Function to read a value from the PCF8591
def read_pcf_value(channel):
    bus.write_byte(pcf_address, 0x40 | channel)
    time.sleep(0.1)  # Allow some time for conversion
    value = bus.read_byte(pcf_address)
    return value

try:
    while True:
        # Read values from all four channels and print them
        for channel in range(4):
            value = read_pcf_value(channel)
            print(f"Value from AIN{channel}: {value}")
        print("\033c", end="")
        time.sleep(0.05)


except KeyboardInterrupt:
    # Handle Ctrl+C to exit the loop
    pass

finally:
    # Close the smbus object
    bus.close()