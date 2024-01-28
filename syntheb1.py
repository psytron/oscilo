import numpy as np
import pyaudio



global t 
global prev_dur 

p = pyaudio.PyAudio()
volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 0.019   # in seconds, may be float

prev_dur = 0.019
f = 440.0        # sine frequency, Hz, may be float
t=0.00001

 

def generate_tone_2(frequency,dur):
    samples = (np.sin(2*np.pi*np.arange(fs*dur)*frequency/fs)).astype(np.float32)
    return pyaudio.paFloat32, samples.tostring()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)


 
def run():
    global t
    global prev_dur
    while True:

        t =  t + 0.001
        x = np.sin(t)
        y = np.cos(t)



        frequency = y / 60.0 * 30 + 2
        future_dur = 0.0005  + ( 0.07 * (x/2) ) 

        dur = future_dur - (  (future_dur - prev_dur)/10 )
        
        print( x, y, frequency , dur  )
        
        format, sound = generate_tone_2(frequency, dur)

        stream.write(sound)
        prev_dur = dur 


if __name__ == "__main__":
    run()
