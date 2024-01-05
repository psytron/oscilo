from smbus2 import SMBus
import time
import asciichartpy
import pandas as pd
# Diagnostic Timeseries for PCF8591 ADC for Analog and I2C read_bytes A0 A1 
bus = SMBus(1)  # 1 indicates /dev/i2c-1
address = 0x48  # replace with your device address
command_A0 = 0x40  # control command for analog pin A0 
command_A1 = 0x41  # control command for analog pin A1 
mesg_df = pd.DataFrame(columns=['A0', 'A1'])

while True:
    # Read from A0
    time.sleep(0.1)  #
    bus.write_byte(address, command_A0)
    time.sleep(0.1)  # wait for ADC to complete
    value_A0 = bus.read_byte(address)
    mesg_df = mesg_df.append({'A0': value_A0}, ignore_index=True)
    print("A0 value:", value_A0 )
    print( asciichartpy.plot ( mesg_df['A0'].tolist()  , {"height":10} ) )
    mesg_df = mesg_df.iloc[1:]

    # Read from A1
    time.sleep(0.1)  #
    bus.write_byte(address, command_A1)
    time.sleep(0.1)  # wait for ADC to complete
    value_A1 = bus.read_byte(address)
    mesg_df = mesg_df.append({'A1': value_A1}, ignore_index=True)
    print("A1 value:", value_A1 )
    print( asciichartpy.plot ( mesg_df['A1'].tolist()  , {"height":10,"colors":[asciichartpy.red]} ) )
    mesg_df = mesg_df.iloc[1:]
    
    
    
    # reset screen 
    print("\033c", end="")
    time.sleep(0.05)