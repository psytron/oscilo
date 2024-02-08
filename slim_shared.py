


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
    sample_rate = 44100
    t = np.linspace(0, 1, sample_rate, False)  # 1 second duration
    sine_wave = np.sin(188 * 2 * np.pi * t)  # 188 Hz sine wave 
    return sine_wave    # Start with an existing NumPy array

def get_mtrx_sig():
    existing_shm = shared_memory.SharedMemory(name='xor')
    mtrx = np.ndarray( (10,), dtype=np.float32, buffer=existing_shm.buf)
    existing_shm2 = shared_memory.SharedMemory(name='sig')
    sig = np.ndarray( (44100,), dtype=np.float32, buffer=existing_shm2.buf)
    return mtrx, sig    


def matrix( evnt ):
    a = np.array( [ 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 , 1.0 ] )  

    
    # RAW ARRAY MONDAY 
    # Create a shared memory array using multiprocessing.RawArray
    # 'd' specifies the typecode (double precision float), and 'a' is the existing numpy array

    # raw_array = multiprocessing.RawArray('d', 100 * sample_rate)  # Create a shared memory array
    # raw_np_array = np.frombuffer(raw_array, dtype=np.float64)  # Create a numpy array from the shared memory array
    # for i in range(100):
    #     raw_np_array[i * sample_rate:(i + 1) * sample_rate] = np.sin(188 * 2 * np.pi * t)  # Fill the array with sine wave audio

    # PARAM CONTROLLER ARRAY
    try:
        existing_shm = shared_memory.SharedMemory(name='xor')
        existing_shm.close()
        existing_shm.unlink()  # Unlink (delete) the existing shared memory object
    except FileNotFoundError:
        pass  # Shared memory with the name 'xor' does not exist, which is fine

    shm = shared_memory.SharedMemory(create=True, size=a.nbytes  , name='xor')
    b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf) # Now create a NumPy array backed by shared memory
    b[:] = a[:]                                            # Copy the original data into shared memory

    # SIGbARR
    sine_wave = get_wave()
    try:
        existing_shm2 = shared_memory.SharedMemory(name='sig')
        existing_shm2.close()
        existing_shm2.unlink()  # Unlink (delete) the existing shared memory object
    except FileNotFoundError:
        pass  
    shm2 = shared_memory.SharedMemory(create=True, size=sine_wave.nbytes  , name='sig')
    c = np.ndarray(sine_wave.shape, dtype=sine_wave.dtype, buffer=shm2.buf)     
    c[:]=sine_wave
    evnt.set()                                             # Signal that the shared memory object is ready
    while True:
        print(' MTRX:  ', b )
        time.sleep(3)









def waveform( evnt ):
    evnt.wait()

    mtrx, sig = get_mtrx_sig()
    
    sample_rate = 44100
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32,channels=1,rate=sample_rate,output=True)    
    dur = 0.001
    freq = 528
    iters = 0
    while True:        
             
        freq = 30+ ( mtrx[8] )
        dur = max(0.0001, 0.1 - (mtrx[9] / 1000))
        # Generate a sinusoidal waveform with frequency 'freq' and duration 'dur'
        # The waveform is sampled at 'sample_rate' and the samples are converted to 32-bit floating point numbers
        frame = np.sin( 2*np.pi*np.arange(sample_rate * dur) * freq / sample_rate )
        # float32 for PyAudio stream.write() 
        # float32: single-precision floating point precision audio process.
        samples = frame # .astype(np.float32)
        


        # NOIZ
        # noiz = np.random.normal(0,2, len(samples))
        #samples = samples + ( noiz / mtrx[8] )

        # YES  Normalize to [-1, 1] range # Apply mid-tread quantization , another knob 
        # this works but needs bounds for mtrx[8] 
        # quant_amt = max(1, mtrx[0])
        # n_samples = samples / np.max(np.abs(samples))
        # x_quantized = np.round(n_samples * quant_amt ) / quant_amt
        # samples = x_quantized
    
        i = iters % 4
        segment_size = len(samples) // 4
        start = i * segment_size
        end = start + segment_size
        samples = samples[start:end]
        iters += 1

        stream.write( samples.tobytes() )
        
        stream.write( sig.tobytes() )
        if iters > 3:
            iters = 0
            print('0')
 
 


def fakerotary( evnt ):
    evnt.wait()

    mtrx , sig  = get_mtrx_sig()
    start_time = time.time()
    while True:
        if time.time() - start_time >= 10:
            print('minute')
            start_time = time.time()
            



def fx( evnt ):
    evnt.wait()
    mtrx, sig = get_mtrx_sig()
    
    iteration_count = 0
    while True:

        wav = get_wave()
                    #quant_amt = max(1, mtrx[0])
        quant_amt = np.random.randint(1, 10)
        
        sig_samples = wav / np.max(np.abs(wav))
        x_quantized = np.round(sig_samples * quant_amt ) / quant_amt
        sig[:] = x_quantized
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
    r = multiprocessing.Process(target=fakerotary, args=( evnt, ))
    f = multiprocessing.Process(target=fx, args=( evnt, ))
    procs.extend([m, w, r, f])
    m.start()
    w.start()
    r.start()
    f.start()        
    #set_realtime_priority( w.pid )
    for proc in procs:
        proc.join()
 


if __name__ == "__main__":
    main()