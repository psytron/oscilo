from pedalboard import Pedalboard, Chorus, Compressor, Delay, Gain, Reverb, Phaser
from pedalboard.io import AudioStream

# Open up an audio stream:
with AudioStream(
  input_device_name="MacBook Air Microphone",  # Guitar interface
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