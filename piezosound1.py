

# Connect one terminal of the piezoelectric buzzer to a GPIO pin on the Raspberry Pi (let's say GPIO 18).
# Connect the other terminal of the buzzer to a ground pin on the Raspberry Pi.
# The following script will generate different frequencies of sound using numpy and send it to the piezoelectric buzzer.

import RPi.GPIO as GPIO
import time
import numpy as np

buzzerPin = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin, GPIO.OUT)

def generate_tone(frequency, duration):
    t = np.linspace(0, duration, int(frequency * duration), False)
    note = np.sin(frequency * t * 2 * np.pi)
    return note

def play_tone(pwm, note, duration):
    for i in note:
        pwm.ChangeFrequency(440 * 2 ** (i / 12))  # Change the frequency
        time.sleep(duration / len(note))  # Wait for the note to end

pwm = GPIO.PWM(buzzerPin, 1)

try:
    pwm.start(1)
    for i in range(-12, 13):
        play_tone(pwm, generate_tone(440 * 2 ** (i / 12), 1), 1)
finally:
    pwm.stop()
    GPIO.cleanup()
