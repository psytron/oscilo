



import os
import time
import random
import subprocess
from multiprocessing import shared_memory, Event, Manager 
import multiprocessing
import numpy as np
import pyaudio




def set_realtime_priority(pid, priority=99):
    try:
        subprocess.run(['sudo', 'chrt', '-f', '-p', str(priority), str(pid)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to set real-time priority: {e}")






def matrix( evnt ):
    # CTL 
    arr = np.array( [ 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 ] )      # Start with an existing NumPy array
    shm = shared_memory.SharedMemory(create=True, size=arr.nbytes  , name='ctl')
    ctl_arr = np.ndarray(arr.shape, dtype=arr.dtype, buffer=shm.buf) # Now create a NumPy array backed by shared memory
    ctl_arr[:] = arr[:]                                            # Copy the original data into shared memory
    # SIG
    gradient = np.linspace(0, 1, 44100, False)  # 1 second duration
    wave = np.sin(68 * 2 * np.pi * gradient)  #  sine wave
    shm2 = shared_memory.SharedMemory(create=True, size=wave.nbytes  , name='sig')
    sig_arr = np.ndarray(wave.shape, dtype=wave.dtype, buffer=shm2.buf)     
    sig_arr[:]=wave
    evnt.set()                                             # Signal that the shared memory object is ready
    while True:
        print(' CTL:  ', ctl_arr[:10] )
        print(' SIG:  ', sig_arr[:10] )
        ctl_arr[0] = float(random.randint(1, 17))
        time.sleep(3)








def rotary( evnt ):
    evnt.wait()
    existing_shm = shared_memory.SharedMemory(name='ctl')
    mtrx = np.ndarray((10,), dtype=np.float64, buffer=existing_shm.buf)

    def update_px( px1, px2 ):
        mtrx[8] = px1
        mtrx[9] = px2
    rotarymod.setup_rotary_listener( 16 , 20, 21 , 23 , 24 , 25 , update_px )






def main():
    procs = []
    manager = Manager()
    evnt = manager.Event()
    m = multiprocessing.Process(target=matrix, args=( evnt, ))
    w = multiprocessing.Process(target=waveform, args=( evnt, ))
    f = multiprocessing.Process(target=fx, args=( evnt, ))    
    procs.append(m)
    procs.append(w)
    procs.append(f)
    m.start()
    w.start()
    f.start()
      
    #set_realtime_priority( w.pid )
    for proc in procs:
        proc.join()
 


if __name__ == "__main__":
    main()