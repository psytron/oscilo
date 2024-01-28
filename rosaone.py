


import numpy as np
import librosa
import sounddevice as sd

# Define the basic parameters for the sine wave
sample_rate = 22050  # Sample rate
duration = 5.0  # Duration of the wave
frequency = 440.0  # Frequency of the wave

# Generate the time values for the wave
t = np.linspace(0, duration, int(sample_rate * duration), False)

# Generate the sine wave
sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

# Play the sine wave
sd.play(sine_wave, sample_rate)

# Pause execution until the sound has finished playing
sd.wait()
