


from multiprocessing import shared_memory, Event, Manager 
import multiprocessing
import numpy as np
import time
import random
import os 

import numpy as np
import pyaudio

import subprocess



def set_realtime_priority(pid, priority=99):
    try:
        subprocess.run(['sudo', 'chrt', '-f', '-p', str(priority), str(pid)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to set real-time priority: {e}")


def matrix( evnt ):
    a = np.array( [ 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 ] )      # Start with an existing NumPy array
    
    # RAW ARRAY MONDAY 
    # Create a shared memory array using multiprocessing.RawArray
    # 'd' specifies the typecode (double precision float), and 'a' is the existing numpy array


    # PARAM CONTROLLER ARRAY
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes  , name='xor')
    b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf) # Now create a NumPy array backed by shared memory
    b[:] = a[:]                                            # Copy the original data into shared memory

    # SIGbARR
    sample_rate = 44100
    t = np.linspace(0, 1, sample_rate, False)  # 1 second duration
    sine_wave = np.sin(188 * 2 * np.pi * t)  # 188 Hz sine wave
    shm2 = shared_memory.SharedMemory(create=True, size=sine_wave.nbytes  , name='sig')
    c = np.ndarray(sine_wave.shape, dtype=sine_wave.dtype, buffer=shm2.buf)     
    c[:]=sine_wave
    evnt.set()                                             # Signal that the shared memory object is ready
    while True:
        print(' MTRX:  ', b )
        time.sleep(3)


def waveform( evnt ):
    evnt.wait()
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray( (10,), dtype=np.float64, buffer=existing_shm.buf)

    existing_shm2 = shared_memory.SharedMemory(name='sig')
    sig = np.ndarray( (44100,), dtype=np.float64, buffer=existing_shm2.buf)
    
    sample_rate = 44100
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32,channels=1,rate=sample_rate,output=True)    
    dur = 0.001
    freq = 528
    iters = 0
    while True:
        freq = 120
        dur = 1
        frame = np.sin( 2*np.pi*np.arange(sample_rate * dur) * freq / sample_rate )
        # float32 for PyAudio stream.write() 
        # float32: single-precision floating point precision audio process.
        samples = frame.astype(np.float32)
        
        fade_start_val = samples[-9]
        # DSP  QuickFade
        fade_out = np.linspace(fade_start_val, 0, 9)
        # Apply the fade out effect to the last 5 samples by multiplying them with the reversed fade_out array
        samples[-9:] = fade_out



        
        stream.write( samples.tobytes() )
        sig=sig.astype(np.float32)
        stream.write( sig.tobytes() )
        
        
        if iters > 10:
            print( samples[:4] , " ]   DUR: ",dur," LEN: ",len(samples)," FRQ: ", freq ,'  [',samples[-4:] )

            iters = 0 
        iters +=1

 




def main():
    procs = []
    manager = Manager()
    evnt = manager.Event()
    m = multiprocessing.Process(target=matrix, args=( evnt, ))
    w = multiprocessing.Process(target=waveform, args=( evnt, ))
    procs.append(m)
    procs.append(w)
    m.start()
    w.start()
      
    #set_realtime_priority( w.pid )
    for proc in procs:
        proc.join()
 


if __name__ == "__main__":
    main()