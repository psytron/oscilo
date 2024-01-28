




 # To install sounddevice module, use the command: pip install sounddevice
import sounddevice as sd


import numpy as np
import time

sample_rate = 44100  # Sample rate
seconds = 3  # Duration of playback
f = 444  # Frequency in Hz

 # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
t = np.linspace(0, seconds, seconds * sample_rate, False)
 # Generate a 440 Hz sine wave
note = np.sin(f * t * 2 * np.pi)
 # Ensure that highest value is in 16-bit range
audio = note * (2**15 - 1) / np.max(np.abs(note))
audio = audio.astype(np.int16)

 # Start playback
sd.play(audio, samplerate=sample_rate)

 # We can't stop the sounddevice stream object, we need to stop the playback
time.sleep(seconds)
sd.stop()