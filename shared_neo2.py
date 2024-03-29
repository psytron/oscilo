


from multiprocessing import shared_memory, Event, Manager 
import multiprocessing
import numpy as np
import time
import random
import os 
#from ads1256 import harvest
import numpy as np
import pyaudio
import rotaryfive1 as rotary
import subprocess



def set_realtime_priority(pid, priority=99):
    try:
        subprocess.run(['sudo', 'chrt', '-f', '-p', str(priority), str(pid)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to set real-time priority: {e}")


def matrix( evnt ):
    a = np.array( [ 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 ] )      # Start with an existing NumPy array
    
    # RAW ARRAY MONDAY 
    # Create a shared memory array using multiprocessing.RawArray
    # 'd' specifies the typecode (double precision float), and 'a' is the existing numpy array
    # shm2 = multiprocessing.RawArray('d', a)
    
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes  , name='xor')
    b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf) # Now create a NumPy array backed by shared memory
    b[:] = a[:]                                            # Copy the original data into shared memory
    evnt.set()                                             # Signal that the shared memory object is ready
    while True:
        print(' Matrix:  ', b )
        time.sleep(3)


 

def worker( evnt ):
    evnt.wait()
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray((9,), dtype=np.float64, buffer=existing_shm.buf)
    sample_rate = 44100
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32,channels=1,rate=sample_rate,output=True)    
    dur = 0.001
    freq = 528
    while True:
        freq = 10+  mtrx[8] 
        dur = 0.05+mtrx[0]#+ ( mtrx[8] /10 )
        samples = (np.sin(2*np.pi*np.arange( sample_rate *dur)*freq/ sample_rate )).astype(np.float32)
        stream.write( samples.tobytes() )



 

def sensor( evnt ):
    evnt.wait()
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray((9,), dtype=np.float64, buffer=existing_shm.buf)
    while True:
        #r = harvest.yo()
        #mtrx[:] = r[:]
        pass
        time.sleep(1)
    


def rotary( evnt ):
    evnt.wait()
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray((9,), dtype=np.float64, buffer=existing_shm.buf)

    def update_px( in_val ):
        mtrx[8] = in_val    
    rotary.setup_rotary_listener( update_px )

    

def main():
    procs = []
    manager = Manager()
    evnt = manager.Event()
    m = multiprocessing.Process(target=matrix, args=( evnt, ))
    w = multiprocessing.Process(target=worker, args=( evnt, ))
    s = multiprocessing.Process(target=sensor, args=( evnt, ))
    r = multiprocessing.Process(target=rotary, args=( evnt, ))
    procs.append(m)
    procs.append(w)
    procs.append(s)
    procs.append(r)
    m.start()
    w.start()
    s.start()
    r.start()        
    set_realtime_priority( w.pid )
    for proc in procs:
        proc.join()
 


if __name__ == "__main__":
    main()