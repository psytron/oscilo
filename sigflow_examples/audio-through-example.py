#!/usr/bin/env python3

#--------------------------------------------------------------------------------
# Example: Audio playthrough, from input to output.
# (Be careful to listen through headphones or feedback might occur.)
#--------------------------------------------------------------------------------
import os 
from signalflow import *

graph = AudioGraph()

#--------------------------------------------------------------------------------
# Read single channel input.
# To specify the audio device to use, add to ~/.signalflow/config:
# 
# [audio]
# input_device_name = "My Device"
#--------------------------------------------------------------------------------
audio_in = AudioIn()

audio_path = os.path.join(os.path.dirname(__file__), "../data", "band.wav")
buf = Buffer(audio_path)

#--------------------------------------------------------------------------------
# Add some ringmod and delay.
#--------------------------------------------------------------------------------
audio_out = audio_in * SineOscillator(13)
audio_out = audio_in * SineOscillator(10) * SineOscillator(23)
audio_out = audio_out # + CombDelay(audio_out, 0.2, 0.8) * 0.3

left = SineOscillator(25.1) * SineOscillator(30)
right = SineOscillator(25.1) * SineOscillator(30) 

right = right * SineLFO(0.5)
left = left * SineLFO( 0.4)
#output = ChannelArray([ audio_out, audio_out ])
output = ChannelArray([ left  ,right ])

graph.play( output )
graph.wait()
