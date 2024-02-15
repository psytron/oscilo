


import os
import time
import random
import subprocess
from multiprocessing import shared_memory, Event, Manager 
import multiprocessing
import numpy as np
import pyaudio
import rotaryencodery6 as rotarymod



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






def waveform( evnt ):
    evnt.wait()

    shm_c = shared_memory.SharedMemory(name='ctl')
    ctl = np.ndarray( (10,), dtype=np.float64, buffer=shm_c.buf)

    shm_s = shared_memory.SharedMemory(name='sig')
    sig = np.ndarray( (44100,), dtype=np.float64, buffer=shm_s.buf)
    
    sample_rate = 44100
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32,channels=1,rate=sample_rate,output=True)    
 
    iters = 0
    lf = 0 
    while True:
        lf = 1000 * np.sin(2 * np.pi * iters / 1000)
        iters += 1
        if iters >= 1000:
            iters = 0
        # freq = 120
        # dur = 1
        # frame = np.sin( 2*np.pi*np.arange(sample_rate * dur) * freq / sample_rate )
        # Create a new ndarray that views the first 22050 elements of sig
        sig_trunc = np.ndarray( (int(ctl[0]*1000),), dtype=np.float64, buffer=shm_s.buf)
        samples = sig_trunc.astype(np.float32)
        stream.write( samples.tobytes() )
        sig=sig.astype(np.float32)
        #stream.write( sig.tobytes() )
        
        print(' buffer:: ',iters % 2)



 
def fx( evnt ):
    evnt.wait()

    shm_c = shared_memory.SharedMemory(name='ctl')
    ctl = np.ndarray( (10,), dtype=np.float64, buffer=shm_c.buf)

    shm_s = shared_memory.SharedMemory(name='sig')
    sig = np.ndarray( (44100,), dtype=np.float64, buffer=shm_s.buf)
    
    i = 0
    while True:
        wav = sig
        quant_amt = ctl[9] #quant_amt = max(1, mtrx[0]) 
        freq = ctl[8]*2
        dur = 1
        frame = np.sin( 2*np.pi*np.arange(44100 * dur) * freq / 44100 )
        sig_samples = frame / np.max(np.abs(frame))
        x_quantized = np.round(sig_samples * np.random.randint(1, 20) ) / quant_amt
        sig[:] = x_quantized
        # Write the updated 'sig' array back to the shared memory
        # existing_shm2.buf[:sig.nbytes] = sig.tobytes()

        
        if( i > 10000 ):
            ctl[0] = np.random.randint(1, 20)
            ctl[1] = np.random.randint(1, 20)
            ctl[2] = np.random.randint(1, 20)
            i = 0
            print(' FX   fx: ',quant_amt, '  ',i)
        i = i +1 
    


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
    r = multiprocessing.Process(target=rotary, args=( evnt, ))    
    procs.append(m)
    procs.append(w)
    procs.append(f)
    procs.append(r)
    m.start()
    w.start()
    f.start()
    r.start()
      
    #set_realtime_priority( w.pid )
    for proc in procs:
        proc.join()
 


if __name__ == "__main__":
    main()