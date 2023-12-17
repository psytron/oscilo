#!/usr/bin/env python3

#------------------------------------------------------------------------
# SignalFlow: Modulation example.
#------------------------------------------------------------------------
from signalflow import *

#------------------------------------------------------------------------
# Create the global processing graph.
#------------------------------------------------------------------------
graph = AudioGraph()

#graph.poll(1)

#------------------------------------------------------------------------
# Create a regular impulse that is used to trigger an envelope and S&H.
#------------------------------------------------------------------------
clock = Impulse(73)
frequency = ScaleLinExp(SineLFO(0.1), 0, 10, 100, 200)
sample_hold = SampleAndHold(frequency, clock)
sine = SineOscillator(sample_hold) * 4.001


clock = Impulse(91)
frequency = ScaleLinExp(SineLFO(0.5), 0, 1, 100, 200)
sample_hold = SampleAndHold(frequency, clock)
sqre = SquareOscillator( sample_hold ) * 4.501

env = ASREnvelope(attack=0.001, sustain=2.001, release=0.1, clock=clock)

#------------------------------------------------------------------------
# Apply the envelope, and stereo pan between speakers.
#------------------------------------------------------------------------

#dc = BiquadFilter(input=0.0, filter_type=SIGNALFLOW_FILTER_TYPE_LOW_PASS, cutoff=440, resonance=0.0, peak_gain=0.0)
# sf = SVFilter(input=0.0, filter_type=SIGNALFLOW_FILTER_TYPE_LOW_PASS, cutoff=440, resonance=0.0)

mono = sine * sqre 

stereo = StereoPanner(mono, SineLFO(0.5, -1, 1))


#------------------------------------------------------------------------
# Add some delay.
#------------------------------------------------------------------------
delay1 = CombDelay(mono, 0.1, 0.8)
delay2 = OneTapDelay(CombDelay(mono, 0.05, 0.8), 0.125)
#stereo = stereo + ChannelArray([ delay1, delay2 ]) * 0.2
stereo = ChannelArray([ delay1, delay2 ]) * 0.2

#------------------------------------------------------------------------
# Play the output.
#------------------------------------------------------------------------
graph.play(mono)
graph.wait()
