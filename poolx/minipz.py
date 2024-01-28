from multiprocessing import Pool
import time
import os

def f(x):
    print( 'proc_',os.getpid(),'.run(  ',x,' )')
    time.sleep(2)

    return x*x*x/x*0.00005/3.14158

if __name__ == '__main__':
    # Create a pool of worker processes
    # The parameter 5 indicates the number of worker processes in the pool
    with Pool(1) as p:
        print(p.map(f, [1, 2, 3,5,7,9,11,13]))