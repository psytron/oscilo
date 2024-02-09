


from multiprocessing import shared_memory, Event, Manager 
import multiprocessing
import numpy as np
import time
import random
import os 

import numpy as np
import pyaudio

import subprocess



def get_mtrx_and_sig():
    existing_shm = shared_memory.SharedMemory(name='ctl')
    mtrx = np.ndarray( (10,), dtype=np.float64, buffer=existing_shm.buf)
    existing_shm2 = shared_memory.SharedMemory(name='sig')
    sig = np.ndarray( (44100,), dtype=np.float64, buffer=existing_shm2.buf)
    return mtrx, sig


def set_realtime_priority(pid, priority=99):
    try:
        subprocess.run(['sudo', 'chrt', '-f', '-p', str(priority), str(pid)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to set real-time priority: {e}")


def matrix( evnt ):
    
    # PARAM CONTROLLER ARRAY
    arr = np.array( [ 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 ] )      # Start with an existing NumPy array
    shm = shared_memory.SharedMemory(create=True, size=arr.nbytes  , name='ctl')
    ctl_arr = np.ndarray(arr.shape, dtype=arr.dtype, buffer=shm.buf) # Now create a NumPy array backed by shared memory
    ctl_arr[:] = arr[:]                                            # Copy the original data into shared memory

    # SIGbARR
    gradient = np.linspace(0, 1, 44100, False)  # 1 second duration
    wave = np.sin(188 * 2 * np.pi * gradient)  # 188 Hz sine wave
    shm2 = shared_memory.SharedMemory(create=True, size=wave.nbytes  , name='sig')
    sig_arr = np.ndarray(wave.shape, dtype=wave.dtype, buffer=shm2.buf)     
    sig_arr[:]=wave
    evnt.set()                                             # Signal that the shared memory object is ready
    while True:
        print(' CTL:  ', ctl_arr[:10] )
        print(' SIG:  ', sig_arr[:10] )
        time.sleep(3)


def waveform( evnt ):
    evnt.wait()
    
    existing_shm = shared_memory.SharedMemory(name='ctl')
    mtrx = np.ndarray( (10,), dtype=np.float64, buffer=existing_shm.buf)

    existing_shm2 = shared_memory.SharedMemory(name='sig')
    sig = np.ndarray( (44100,), dtype=np.float64, buffer=existing_shm2.buf)
    
    sample_rate = 44100
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32,channels=1,rate=sample_rate,output=True)    
 
 
    iters = 0
    while True:
        freq = 120
        dur = 1
        frame = np.sin( 2*np.pi*np.arange(sample_rate * dur) * freq / sample_rate )
        # float32 for PyAudio stream.write() 
        # float32: single-precision floating point precision audio process.
        samples = frame.astype(np.float32)
        
        fade_start_val = samples[-9]
        # DSP  QuickFade
        fade_out = np.linspace(fade_start_val, 0, 9)
        # Apply the fade out effect to the last 5 samples by multiplying them with the reversed fade_out array
        samples[-9:] = fade_out



        
        stream.write( samples.tobytes() )
        sig=sig.astype(np.float32)
        stream.write( sig.tobytes() )
        
        
        if iters > 10:
            print( samples[:4] , " ]   DUR: ",dur," LEN: ",len(samples)," FRQ: ", freq ,'  [',samples[-4:] )

            iters = 0 
        iters +=1

 
def fx( evnt ):
    evnt.wait()

    existing_shm = shared_memory.SharedMemory(name='ctl')
    mtrx = np.ndarray( (10,), dtype=np.float64, buffer=existing_shm.buf)

    existing_shm2 = shared_memory.SharedMemory(name='sig')
    sig = np.ndarray( (44100,), dtype=np.float64, buffer=existing_shm2.buf)
    
    iteration_count = 0
    while True:

        wav = sig
                    #quant_amt = max(1, mtrx[0])
        quant_amt = np.random.randint(1, 10)
        
        sig_samples = wav / np.max(np.abs(wav))
        x_quantized = np.round(sig_samples * quant_amt ) / quant_amt
        #sig[:] = x_quantized
        # Write the updated 'sig' array back to the shared memory
        # existing_shm2.buf[:sig.nbytes] = sig.tobytes()
        # iteration_count=0
        print('fx: ',quant_amt, '  ',iteration_count)
        time.sleep(5)






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