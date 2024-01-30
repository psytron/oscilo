

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
        pwm.ChangeFrequency(240 * 2 ** (i / 12))  # Change the frequency
        time.sleep(duration / len(note))  # Wait for the note to end

# This line initializes a PWM (Pulse Width Modulation) instance on the GPIO pin connected to the buzzer.
# The PWM instance is used to control the frequency of the electrical signal sent to the buzzer, which in turn controls the sound produced by the buzzer.
# The first argument, 'buzzerPin', is the GPIO pin number to which the buzzer is connected.
# The second argument, '1', is the initial frequency of the PWM signal in Hertz. This frequency will be changed later in the code to produce different tones.
pwm = GPIO.PWM(buzzerPin, 1)

try:
    pwm.start(1)
    for i in range(-12, 13):
        play_tone(pwm, generate_tone(240 * 2 ** (i / 12), 1), 1)
finally:
    pwm.stop()
    GPIO.cleanup()
