


import RPi.GPIO as GPIO
import time

# Use the Broadcom SOC channel, which maps to the GPIO numbers on the Raspberry Pi.
GPIO.setmode(GPIO.BCM)

# List of GPIO pins you want to test.
pins = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21]

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    
    # blink
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)

GPIO.cleanup()