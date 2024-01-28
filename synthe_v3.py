import numpy as np
import pyaudio
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
print('erun ')
p = pyaudio.PyAudio()
volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 0.019   # in seconds, may be float
prev_dur = 0.019
f = 440.0        # sine frequency, Hz, may be float
drifter = { 'x':0 , 'y':0 }

def generate_tone(frequency):
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*frequency/fs)).astype(np.float32)

    #samples = (np.sign(np.sin(2*np.pi*np.arange(fs*duration)*frequency/fs))).astype(np.float32)
    return pyaudio.paFloat32, samples.tostring()

def generate_tone_2(frequency,dur):
    samples = (np.sin(2*np.pi*np.arange(fs*dur)*frequency/fs)).astype(np.float32)
    return pyaudio.paFloat32, samples.tostring()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)





while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    drifter['x'] = drifter['x'] - (  ( drifter['x']-x) /200  )
    drifter['y'] = drifter['y'] - (  ( drifter['y']-y) /200  )    

    frequency = drifter['y'] / 60.0 * 300 + 20
    #future_dur = 0.00001 + ( 0.0001 * (drifter['x']/2) ) 

    dur = drifter['x'] * 0.0001
    
    print( x, y, frequency , dur  , drifter )
    
    format, sound = generate_tone_2(frequency, dur)

    stream.write(sound)
    prev_dur = dur 
