


import sounddevice as sd
import matplotlib.pylot as plt

while True: 
    rec = sd.rec( int(44100*0.01),44100,1)
    plt.plot(rec)
    plt.axis('off')
    plt.pause(0.01)
    plt.clf()