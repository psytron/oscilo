





from smbus2 import SMBus
import time
import asciichartpy
# Diagnostic Timeseries for PCF8591 ADC for Analog and I2C read_bytes A0 A1 
bus = SMBus(1)  # 1 indicates /dev/i2c-1
address = 0x48  # replace with your device address
command_A0 = 0x40  # control command for analog pin A0 
command_A1 = 0x41  # control command for analog pin A1 
mesg_arr_0 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
mesg_arr_1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 

while True:
    # Read from A0
    bus.write_byte(address, command_A0)
    time.sleep(0.1)  # wait for ADC to complete
    value_A0 = bus.read_byte(address)
    mesg_arr_0.append( value_A0 )
    print("A0 value:", value_A0 )
    print( asciichartpy.plot ( mesg_arr_0  , {"height":10} ) )
    mesg_arr_0 = mesg_arr_0[1:]

    # Read from A1
    bus.write_byte(address, command_A1)
    time.sleep(0.1)  # wait for ADC to complete
    value_A1 = bus.read_byte(address)
    mesg_arr_1.append(  value_A1 )
    print("A1 value:", value_A1 )
    print( asciichartpy.plot ( mesg_arr_1  , {"height":10,"colors":[asciichartpy.red]} ) )
    mesg_arr_1 = mesg_arr_1[1:]
    
    
    
    # reset screen 
    print("\033c", end="")
    time.sleep(0.05)