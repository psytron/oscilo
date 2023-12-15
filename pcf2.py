
import board
import subprocess
import adafruit_pcf8591.pcf8591 as PCF
from adafruit_pcf8591.analog_in import AnalogIn
from adafruit_pcf8591.analog_out import AnalogOut
import asciichartpy
import time

i2c = board.I2C()  # uses board.SCL and board.SDA
#i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
pcf = PCF.PCF8591(i2c)

pcf_in_0 = AnalogIn(pcf, PCF.A0) #  reference voltage 
pcf_in_1 = AnalogIn(pcf, PCF.A1)
pcf_out = AnalogOut(pcf, PCF.OUT)

print( 'booting: ')
print( PCF.A0 , PCF.OUT , PCF )

volt_arr_0 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
volt_arr_1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
while True:
   
    pcf_out.value = 65535
    
    raw_value_0 = pcf_in_0.value
    raw_value_1 = pcf_in_1.value
    
    scaled_value_0 = (raw_value_0 / 65535) * pcf_in_0.reference_voltage
    scaled_value_1 = (raw_value_1 / 65535) * pcf_in_1.reference_voltage

    print( " A0 R:", raw_value_0 )
    print( " A0 S:", scaled_value_0 )
    volt_arr_0.append(  scaled_value_0 )
    print( asciichartpy.plot ( volt_arr_0  , {"height":10} ) )
    print( "                     ")
    print( " A1 R:", raw_value_1 )
    print( " A1 S:", scaled_value_1)  
    
    volt_arr_1.append(  scaled_value_1 )
    print( asciichartpy.plot ( [volt_arr_0 ,volt_arr_1]  , {"height":10,"colors":[asciichartpy.green,asciichartpy.red]} ) )


    volt_arr_0= volt_arr_0[1:]
    volt_arr_1= volt_arr_1[1:]
    print("\033c", end="")
    time.sleep(0.05)





config = {

    "offset":  3,          # axis offset from the left (min 2)
    #"padding": '       ',  // padding string for label formatting (can be overrided)
    "height":  10        #  any height you want#
}
