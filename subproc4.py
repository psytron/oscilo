

import multiprocessing as mp
from multiprocessing import shared_memory
import numpy as np
import os

import time

class Worker:
    def __init__(self, name, shared_ix):
        self.name = name
        self.shared_ix = shared_ix
        self.iterations = 0 

    def run(self):
        while True:
            self.shared_ix[0] = self.shared_ix[0] + 1
            self.iterations += 1 
            print('')
            print('  '  )
            print(self.name,' i : ' ,self.iterations )
            print(self.name,' x : ' ,self.shared_ix[0]  )
            time.sleep(1)

            if( self.iterations >2):

                os._exit(0)



class Mtrx:
    def __init__(self, name, shared_ix):
        self.name = name
        self.shared_ix = shared_ix

    def run(self):
        print(f"WFFR {self.name} is running")




# Create a shared memory block for a single integer
shm = shared_memory.SharedMemory(create=True, size=np.dtype(int).itemsize)

# Now create a NumPy array backed by shared memory
shared_ix = np.ndarray((1,), dtype=int, buffer=shm.buf)

# Initialize the shared integer to 0
shared_ix[0] = 0

# Create worker instances
worker1 = Worker("Onero", shared_ix)
worker2 = Worker("Deusx", shared_ix)

# Create processes
p1 = mp.Process(target=worker1.run)
p2 = mp.Process(target=worker2.run)

if __name__ == '__main__':
    # Start processes
    p1.start()
    p2.start()

    # Join processes
    p1.join()
    p2.join()



# Cleanup the shared memory block
shm.close()
shm.unlink()
