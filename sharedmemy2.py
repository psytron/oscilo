


# In the first Python interactive shell
from multiprocessing import shared_memory
import multiprocessing
import numpy as np
import time
import random
###
def matrix( ):
    a = np.array([1, 3, 8])  # Start with an existing NumPy array
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes  , name='xor')
    b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf) # Now create a NumPy array backed by shared memory
    b[:] = a[:]  # Copy the original data into shared memory

 
####
def worker( ):
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray((3,), dtype=np.int64, buffer=existing_shm.buf)
    while True: 
        i=9
        print( mtrx , random.randint(1, 100) )


def sensor( ):
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray((3,), dtype=np.int64, buffer=existing_shm.buf)
    
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                x, _ = pygame.mouse.get_pos()
                mtrx[0] = x

        pygame.display.flip()
        clock.tick(60)
    mtrx[0] = random.randint(1000, 10000)
    #print(mtrx)





def main():
    procs = []
    m = multiprocessing.Process(target=matrix, args=())
    procs.append(m)
    m.start()
    m.join()

    time.sleep(2)

    w = multiprocessing.Process(target=worker, args=())
    procs.append(w)
    w.start()
    
    
    s = multiprocessing.Process(target=sensor, args=())
    procs.append(s)
    s.start()
    s.join()
if __name__ == "__main__":
    main()
