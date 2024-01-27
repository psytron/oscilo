

import numpy as np
import pyaudio



def run():
    sample_rate = 44100
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32,channels=1,rate=sample_rate,output=True)    
    dur = 0.1
    freq = 528
    while True:
        samples = (np.sin(2*np.pi*np.arange( sample_rate *dur)*freq/ sample_rate )).astype(np.float32)
        stream.write( samples.tobytes() )
 

if __name__ == "__main__":
    run()
