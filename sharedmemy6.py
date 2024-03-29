


# In the first Python interactive shell
from multiprocessing import shared_memory, Event, Manager 

import multiprocessing
import numpy as np
import time
import random
import os 
from ads1256 import harvest

import numpy as np
import pyaudio




def matrix( evnt ):
    a = np.array( [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0] )      # Start with an existing NumPy array
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes  , name='xor')
    b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf) # Now create a NumPy array backed by shared memory
    b[:] = a[:]                                            # Copy the original data into shared memory
    evnt.set()                                             # Signal that the shared memory object is ready
    while True:
        print(' Matrix Shared Proc:  ', os.getpid(), b )
        time.sleep(3)


 

def worker( evnt ):
    evnt.wait()
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray((8,), dtype=np.float64, buffer=existing_shm.buf)
    sample_rate = 44100
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32,channels=1,rate=sample_rate,output=True)    
    dur = 0.01
    freq = 528
    while True:
        freq = 20+  mtrx[0] *100 
        dur = 0.05 + ( mtrx[1] /10 )
        samples = (np.sin(2*np.pi*np.arange( sample_rate *dur)*freq/ sample_rate )).astype(np.float32)
        stream.write( samples.tobytes() )



 

def sensor( evnt ):
    evnt.wait()
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray((8,), dtype=np.float64, buffer=existing_shm.buf)
    while True:
        r = harvest.yo()
        mtrx[:] = r[:]
    




def main():
    manager =  Manager()
    evnt = manager.Event()
    procs = []

    m = multiprocessing.Process(target=matrix, args=( evnt, ))
    w = multiprocessing.Process(target=worker, args=( evnt, ))
    s = multiprocessing.Process(target=sensor, args=( evnt, ))
    procs.append(m)
    m.start()
    procs.append(w)
    w.start()
    procs.append(s)
    s.start()
    
    print( procs )
    for proc in procs:
        proc.join()

    #manager.shutdown()

if __name__ == "__main__":
    main()
