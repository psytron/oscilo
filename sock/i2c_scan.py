


import smbus

# Create an SMBus object
bus = smbus.SMBus(1)  # Use 1 for Raspberry Pi 3, 0 for Raspberry Pi 1 or 2

for i in range(128):
    try:
            # Try to read from each possible I2C address
            bus.read_byte(i)
            print(f"Device found at address 0x{i:02X}")

    except IOError:
        print(f"NO Device  at address 0x{i:02X}")
        pass  # No device at this address

    finally:
        # Clean up resources
        bus.close()


