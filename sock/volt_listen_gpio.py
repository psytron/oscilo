



import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
GPIO.setup(17, GPIO.IN)

try:
    while True:
        # Read the GPIO pin 18 to get the voltage
        voltage = GPIO.input(18)
        
        # Read I2C data from another GPIO pin
        i2c_data_2 = GPIO.input(17)
        print("Voltage: ", voltage)
        print(" i2c_data ", i2c_data_2 )
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
