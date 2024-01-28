import numpy as np
import pyaudio
from pedalboard import Pedalboard

p = pyaudio.PyAudio()
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
f = 60.0        # sine frequency, Hz, must be float

def generate_tone(frequency):
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*frequency/fs)).astype(np.float32)
    return pyaudio.paFloat32, samples.tobytes()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# Create a new pedalboard.
pb = Pedalboard()

while True:
    format, sound = generate_tone(f)
    sound_array = np.frombuffer(sound, dtype=np.float32)
    processed_sound = pb.process(sound_array, sample_rate=fs)
    processed_sound = processed_sound.astype(np.float32).tobytes()
    stream.write(processed_sound)

