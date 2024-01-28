


import numpy as np
import pyaudio
from pedalboard import Pedalboard, Compressor
from pedalboard import Pedalboard, Chorus, Compressor, Delay, Gain, Reverb, Phaser

p = pyaudio.PyAudio()
volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float

def generate_tone_2(frequency,dur):
    samples = (np.sin(2*np.pi*np.arange(fs*dur)*frequency/fs)).astype(np.float32)
    return pyaudio.paFloat32, samples.tobytes()

    # Opening a new audio stream using PyAudio's open method.
    # The parameters are as follows:
    # format: The sample format for the stream. Here we are using pyaudio.paFloat32 which represents 32-bit float samples.
    # channels: The number of channels for the stream. Here we are using 1 for mono audio.
    # rate: The sample rate for the stream. Here we are using the variable fs which is set to 44100 Hz.
    # output: Whether the stream is an output stream. Here we are setting it to True as we are generating audio.
    # output_device_index: The index of the output device to use. Here we are using the default output device.
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)




# Create a new pedalboard.
pb = Pedalboard([
    Chorus(),
    Phaser(),
    Reverb(room_size=1.0)    
])

while True:
    format , sound = generate_tone_2(880, 0.01)
    # Process the sound with the pedalboard.
    sound_array = np.frombuffer(sound, dtype=np.float32)
    processed_sound = pb.process(sound_array, sample_rate=fs)
    #processed_sound = sound_array
    # Convert the processed sound to bytes and write it to the stream.
    stream.write(processed_sound )