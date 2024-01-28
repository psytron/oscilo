from pedalboard import Pedalboard, Chorus, Compressor, Delay, Gain, Reverb, Phaser
from pedalboard.io import AudioStream
import numpy as np

import pyaudio

p = pyaudio.PyAudio()
volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 0.019   # in seconds, may be float
prev_dur = 0.019
f = 440.0        # sine frequency, Hz, may be float
drifter = { 'x':0 , 'y':0 }


def generate_tone_2(frequency,dur):
    samples = (np.sin(2*np.pi*np.arange(fs*dur)*frequency/fs)).astype(np.float32)
    return pyaudio.paFloat32, samples.tostring()



p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                input=True,
                output=True)


format, sound = generate_tone_2(880, 0.01)
stream.write(sound)

with AudioStream(
  input_device_name="In1",  # Guitar interface
  output_device_name="MacBook Air Speakers",
  allow_feedback=True
) as stream:
  # Audio is now streaming through this pedalboard and out of your speakers!
  stream.plugins = Pedalboard([
      Compressor(threshold_db=-50, ratio=25),
      Gain(gain_db=60),
      Chorus(),
      Phaser(),
      Reverb(room_size=0.25)
  ])
  input("Press enter to stop streaming...")