

# Connect one terminal of the piezoelectric buzzer to a GPIO pin on the Raspberry Pi (let's say GPIO 18).
# Connect the other terminal of the buzzer to a ground pin on the Raspberry Pi.
# The following script will generate different frequencies of sound using numpy and send it to the piezoelectric buzzer.

import RPi.GPIO as GPIO
import time
import numpy as np

buzzerPin = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin, GPIO.OUT)
pwm = GPIO.PWM(buzzerPin, 40)

try:
    pwm.start(80)
    time.sleep(1)
    pwm.ChangeFrequency(240) 
    time.sleep(1)
    pwm.ChangeFrequency(444) 
    time.sleep(1)

finally:
    pwm.stop()
    GPIO.cleanup()
