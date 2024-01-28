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
import time
 

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    
    drifter['x'] = drifter['x'] - (  ( drifter['x']-x) /200  )
    drifter['y'] = drifter['y'] - (  ( drifter['y']-y) /200  )
    
    print( x , y  ,  drifter['x'] , drifter['y'] )

    time.sleep(0.01)
