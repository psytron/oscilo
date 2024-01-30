

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
    # This function generates a tone of a given frequency and duration.
    # 'frequency' is the frequency of the tone in Hertz.
    # 'duration' is the duration of the tone in seconds.
    # 't' is a numpy array of time values at which the tone is sampled.
    # 'note' is a numpy array representing the tone.
    t = np.linspace(0, duration, int(frequency * duration), False)  # Generate time values
    note = np.sin(frequency * t * 2 * np.pi)  # Generate the tone
    return note  # Return the generated tone

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
    pwm.start(40)
    
    time.sleep(1)
    pwm.ChangeFrequency(240) 
    time.sleep(1)
    pwm.ChangeFrequency(444) 
    time.sleep(1)

    # The following loop plays a series of tones, each with a different frequency.
    # The range of frequencies is determined by the range function, which generates a sequence of integers from -12 to 12.
    # The frequency of each tone is calculated as 240 * 2 ** (i / 12), where 'i' is the current integer in the sequence.
    # The reason for using negative values in the range is to generate lower frequencies.
    # When 'i' is negative, 2 ** (i / 12) is less than 1, which results in a frequency lower than 240 Hz.
    # When 'i' is positive, 2 ** (i / 12) is greater than 1, which results in a frequency higher than 240 Hz.
    # When 'i' is 0, the frequency is exactly 240 Hz.
    for i in range(-12, 13):
        play_tone(pwm, generate_tone(240 * 2 ** (i / 12), 1), 1)
finally:
    pwm.stop()
    GPIO.cleanup()
