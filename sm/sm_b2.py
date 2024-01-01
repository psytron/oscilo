


from smbus2 import SMBus

# Open i2c bus 1 and read one byte from address 80, offset 0
bus = SMBus(1)
# The function read_byte_data is used to read a single byte from a device at a specific address.
# The first parameter '80' is the address of the device on the I2C bus.
 # The second parameter '0' is the register on the device to read from.
 # A register is a small amount of storage available on the I2C device. 
 # The number of registers varies per device, but each register has a unique address.
b = bus.read_byte_data(80, 0)
print(b)
bus.close()