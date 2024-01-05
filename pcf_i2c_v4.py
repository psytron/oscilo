from smbus2 import SMBus
import time
import asciichartpy
import pandas as pd
# Diagnostic Timeseries for PCF8591 ADC for Analog and I2C read_bytes A0 A1 
bus = SMBus(1)  # 1 indicates /dev/i2c-1
address = 0x48  # replace with your device address
command_A0 = 0x40  # control command for analog pin A0 
command_A1 = 0x41  # control command for analog pin A1 
df = pd.DataFrame(columns=['A0', 'A1'])
df['A0'] = [0]*30
df['A1'] = [0]*30


while True:
    # READ A0
    bus.write_byte( address, command_A0 )
    time.sleep(0.1)  # AWAIT ADC 
    value_A0 = bus.read_byte( address )
    
    # READ A1
    bus.write_byte( address, command_A1 )
    time.sleep(0.1)  # AWAIT ADC 
    value_A1 = bus.read_byte(address)

    # ADD DATA ROWS 
    new_rows = pd.DataFrame([{'A0': value_A0, 'A1': value_A1}])
    df = pd.concat([df, new_rows], ignore_index=True)    

    # CALCULATE EXPONENTIAL WEIGHTED MOVING AVERAGE FOR A0
    df['A0MA'] = df['A0'].ewm(span=30).mean()
    df['A1MA'] = df['A1'].ewm(span=30).mean()

    # CALCULATE MOVING AVERAGE
    dfma = df.rolling(window=20).mean()

    # DISPLAY DF 
    print( "A0 value:", value_A0 )
    print( asciichartpy.plot ( df['A0MA'].tolist()  , {"height":10,"colors":[ asciichartpy.purple ]} ) )
    print( "A1 value:", value_A1 )
    print( asciichartpy.plot ( df['A1MA'].tolist()  , {"height":10,"colors":[ asciichartpy.red    ]} ) )
    
    # TRUNC DF 
    df =df.iloc[1:]
    
    # RESET SCREEN
    print("\033c", end="")
    time.sleep(0.05)