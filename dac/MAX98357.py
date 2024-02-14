

import pygame
import RPi.GPIO as GPIO

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Initialize the pygame mixer
pygame.mixer.init()

# Load the sound file
sound = pygame.mixer.Sound('your_sound_file.wav')

# Play the sound
GPIO.output(18, GPIO.HIGH)
sound.play()

# Wait for the sound to finish
while pygame.mixer.get_busy():
    pass

# Turn off the amplifier
GPIO.output(18, GPIO.LOW)