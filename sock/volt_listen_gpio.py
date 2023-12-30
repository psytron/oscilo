



import RPi.GPIO as GPIO
import time
import smbus

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.IN)

try:
    while True:
        # Read I2C data from another GPIO pin
        i2c_data_2 = GPIO.input(17)
        # Read the GPIO pin 18 to get the voltage
        voltage = GPIO.input(18)

        # Read I2C from another pin
        bus = smbus.SMBus(1)
        address = 0x04
        i2c_data = bus.read_byte(address)



        print("Voltage: ", voltage)
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
