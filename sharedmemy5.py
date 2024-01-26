


# In the first Python interactive shell
from multiprocessing import shared_memory, Event, Manager 

import multiprocessing
import numpy as np
import time
import random
from ads1256 import harvest



def matrix( evnt ):
    a = np.array([1, 3, 8])  # Start with an existing NumPy array
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes  , name='xor')
    b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf) # Now create a NumPy array backed by shared memory
    b[:] = a[:]  # Copy the original data into shared memory
    evnt.set()  # Signal that the shared memory object is ready


 

def worker( evnt ):
    evnt.wait()
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray((3,), dtype=np.int64, buffer=existing_shm.buf)


    while True: 
        i=9
        print( mtrx , random.randint(1, 100) )
        print( harvest.read() )




def sensor( evnt ):
    evnt.wait()
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray((3,), dtype=np.int64, buffer=existing_shm.buf)
    




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
    
    for proc in procs:
        proc.join()

    manager.shutdown()

if __name__ == "__main__":
    main()
