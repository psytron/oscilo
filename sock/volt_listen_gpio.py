



import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

try:
    while True:
        voltage = GPIO.input(18)
        print("Voltage: ", voltage)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
