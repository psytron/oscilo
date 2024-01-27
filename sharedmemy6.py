


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
    a = np.array( [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0] )  # Start with an existing NumPy array
    print( ' dtype: ', a.dtype )
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes  , name='xor')
    b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf) # Now create a NumPy array backed by shared memory
    b[:] = a[:]  # Copy the original data into shared memory
    evnt.set()  # Signal that the shared memory object is ready
    while True:
        time.sleep(1)
        print(' Matrix Shared Proc:  ', os.getpid(), b )
        pass


 

def worker( evnt ):
    import numpy as np
    import pyaudio

    evnt.wait()
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray((8,), dtype=np.float64, buffer=existing_shm.buf)
    sample_rate = 44100
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32,channels=1,rate=sample_rate,output=True)    
    dur = 0.01
    freq = 528
    while True:
        freq = 120+  mtrx[0] *10 
        samples = (np.sin(2*np.pi*np.arange( sample_rate *dur)*freq/ sample_rate )).astype(np.float32)
        stream.write( samples.tobytes() )



 

def sensor( evnt ):
    # This line makes the process wait until the event is set in another process.
    # It ensures that the shared memory is ready before this process tries to access it.
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
    procs.append(m)
    m.start()

    time.sleep(4)

    w = multiprocessing.Process(target=worker, args=( evnt, ))
    procs.append(w)
    w.start()
    
    
    s = multiprocessing.Process(target=sensor, args=( evnt, ))
    procs.append(s)
    s.start()
    
    print( procs )
    for proc in procs:
        proc.join()

    #manager.shutdown()

if __name__ == "__main__":
    main()
