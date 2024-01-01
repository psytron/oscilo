

import random
from pyo import *

# Initialize the audio server
s = Server().boot()

# Create a sine wave oscillator
osc = Sine(freq=random.choice([220, 440, 880]))

# Create reverb and delay effects
rev = Freeverb(osc, size=0.85, damp=0.6, bal=0.3).out()
del = Delay(osc, delay=0.25, feedback=0.5).out()

# Function to generate and play MIDI notes
def play_random_note():
    midinote = random.randint(60, 72)  # MIDI notes between C4 and C5
    osc.freq = midinote.midiToHz()
    metro.play()

# Create a metro object to schedule note events
metro = Metro(time=random.uniform(0.5, 1.5), poly=1).play()
metro.callback = play_random_note

# Start the audio server
s.start()




# Keep the program running until interrupted
while True:
    time.sleep(100)