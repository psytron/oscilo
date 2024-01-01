



import random
import time
from synthesizer import Player, Synthesizer, Waveform, Writer, Effect, EffectsBuilder

synth = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
effects = EffectsBuilder().with_reverb(0.5).with_chorus(0.5).build()
player = Player(effect=effects)
player.open_stream()

while True:
    note = random.randint(40, 100)
    player.play_wave(synth.generate_constant_wave(note, 1.0))
    time.sleep(0.5)
