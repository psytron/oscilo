


# In the first Python interactive shell
from multiprocessing import shared_memory, Event, Manager 

import multiprocessing
import numpy as np
import time
import random
import os 
#from ads1256 import harvest



def matrix( evnt ):
    a = np.array([1, 3, 8])  # Start with an existing NumPy array
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes  , name='xor')
    b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf) # Now create a NumPy array backed by shared memory
    b[:] = a[:]  # Copy the original data into shared memory
    evnt.set()  # Signal that the shared memory object is ready
    while True:
        time.sleep(5)
        print(' Matrix Shared Proc:  ', os.getpid() , b )
        pass


 

def worker( evnt ):
    evnt.wait()
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray((3,), dtype=np.int64, buffer=existing_shm.buf)


    while True: 
        i=9
        time.sleep(0.5)
        print( 'MATRIX: ', mtrx , random.randint(1, 100) )
        




def sensor( evnt ):
    # This line makes the process wait until the event is set in another process.
    # It ensures that the shared memory is ready before this process tries to access it.
    evnt.wait()
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray((3,), dtype=np.int64, buffer=existing_shm.buf)
    while True:
        time.sleep(2)
        print('sensor ping')
    




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
