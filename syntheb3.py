

import numpy as np
import pyaudio



def run():
 

    p = pyaudio.PyAudio()
 
    sample_rate = 44100       # sampling rate, Hz, must be integerf
 

    def generate_tone(frequency,dur):
        samples = (np.sin(2*np.pi*np.arange( sample_rate *dur)*frequency/ sample_rate )).astype(np.float32)
        return samples.tobytes()

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sample_rate,
                    output=True)    
    while True:

        stream.write( generate_tone( 0.7, 0.03 ) )
 

if __name__ == "__main__":
    run()
