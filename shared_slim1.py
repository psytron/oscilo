


from multiprocessing import shared_memory, Event, Manager 
import multiprocessing
import numpy as np
import time
import random
import os 
import numpy as np
import pyaudio
import subprocess


def get_wave():
    rows = 44100
    t = np.linspace(0, 1, rows, False)
    mult_res  = 88 * 2 * np.pi * t
    sine_wave = np.sin(  mult_res ).astype( np.float32 )    # 188 Hz sine wave 
    print( 'sine_wave dtype ', sine_wave.dtype )
    return sine_wave   # Start with an existing NumPy array

def get_mtrx_and_sig():
    
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray( (10,) , dtype=np.float32, buffer=existing_shm.buf)
    
    existing_shm2 = shared_memory.SharedMemory(name='sig')
    sig = np.ndarray( (44100,) , dtype=np.float32, buffer=existing_shm2.buf)
    
    return mtrx, sig    


def matrix( evnt ):
    # PARAMETERS
    try:
        existing_shm = shared_memory.SharedMemory(name='xor')
        existing_shm.close()
        existing_shm.unlink()                                   # Unlink (delete) the existing shared memory object
    except FileNotFoundError:
        pass  #                                                    Shared memory with the name 'xor' does not exist, which is fine
    a = np.array( [ 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 ] )  
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes  , name='xor')
    b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)      # Now create a NumPy array backed by shared memory
    b[:] = a[:] 
                                  # Copy the original data into shared memory


    # SIGNAL 
    sine_wave = get_wave()
    try:
        existing_shm2 = shared_memory.SharedMemory(name='sig')
        existing_shm2.close()
        existing_shm2.unlink() 
    except FileNotFoundError:
        pass  
    shm2 = shared_memory.SharedMemory(create=True, size=sine_wave.nbytes  , name='sig')
    c = np.ndarray(sine_wave.shape, dtype=sine_wave.dtype, buffer=shm2.buf)     
    
    #c[:]=sine_wave
        # Generate a numpy array of random values
    random_values = np.random.uniform(low=0.0, high=1.0, size=(44100,)).astype(np.float32)
    c[:] = random_values      
    evnt.set()                                             # Signal that the shared memory object is ready
    while True:
        print(' MTRX:  ', b )
        time.sleep(3)



def waveform( evnt ):
    evnt.wait()
    pa =  pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32,channels=1,rate=44100,output=True)    
    mtrx, sig = get_mtrx_and_sig()
    l = 9
    while True:        
        print( 'stream write attempt ' , sig.dtype )
        print( ' jiji ')
        print( 'stream write attempt ' , sig[::5000]  )
        stream.write( sig.tobytes() )
        print( ' stream write done '  , sig.shape)
 
 


def fakerotary( evnt ):
    evnt.wait()

    mtrx , sig  = get_mtrx_and_sig()
    start_time = time.time()
    while True:
        if time.time() - start_time >= 10:
            print('minute')
            start_time = time.time()
            

def fx( evnt ):
    evnt.wait()
    mtrx, sig = get_mtrx_and_sig()
    
    iteration_count = 0
    while True:

        wav = get_wave()
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
    #r = multiprocessing.Process(target=fakerotary, args=( evnt, ))
    #f = multiprocessing.Process(target=fx, args=( evnt, ))
    procs.extend([m, w])
    m.start()
    w.start()
    #r.start()
    #f.start()        
    #set_realtime_priority( w.pid )
    for proc in procs:
        proc.join()
 


if __name__ == "__main__":
    main()