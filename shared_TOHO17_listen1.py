


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
        quant_amt = ctl[0] #quant_amt = max(1, mtrx[0]) 
        freq = ctl[2]*2
        dur = 1
        frame = np.sin( 2*np.pi*np.arange(44100 * dur) * freq / 44100 )
        sig_samples = frame / np.max(np.abs(frame))
        x_quantized = np.round(sig_samples * np.random.randint(1, 20) ) / quant_amt
        sig[:] = x_quantized
        # Write the updated 'sig' array back to the shared memory
        # existing_shm2.buf[:sig.nbytes] = sig.tobytes()

        #print('fx: ',quant_amt, '  ',i)
        if( i > 1000 ):
            ctl[0] = np.random.randint(1, 20)
            ctl[1] = np.random.randint(1, 20)
            ctl[2] = np.random.randint(1, 20)
            i = 0
        i = i +1 
    



def socketlisten( evnt ):
    import socket
    from datetime import datetime
    import json
                
    evnt.wait()

    shm_c = shared_memory.SharedMemory(name='ctl')
    ctl = np.ndarray( (10,), dtype=np.float64, buffer=shm_c.buf)

    shm_s = shared_memory.SharedMemory(name='sig')
    sig = np.ndarray( (44100,), dtype=np.float64, buffer=shm_s.buf)    

    HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f'Connected by {addr}')
            while True:
                # 1024 for conn.recv max data one time 
                # The recv() method in socket programming is used to receive data from the socket. 
                # The method takes one argument, the maximum amount of data to be received at once. 
                # This is necessary because the incoming data could be of arbitrary length, and we do not want to overflow the receiving buffer.
                # Here, we are receiving data up to 1024 bytes. If the incoming data is more than 1024 bytes, 
                # the recv() method will receive the first 1024 bytes and the rest of the data will be received in the next call to recv().
                # Yes, the recv() method is a blocking method by default. 
                # This means that if no data is available to be received, the method will wait until there is data.
                # If you want to make it non-blocking, you can set the socket to non-blocking mode with setblocking(0) 
                # or use the settimeout() method to set a timeout.
                # data = conn.recv(1024, socket.MSG_DONTWAIT)
                data = conn.recv(1024)
                if not data:
                    break
                dat = data.decode()
                datl = json.loads( dat )
                print(f'Received: { datl["message"] }')
                
                sent_time = datetime.strptime(datl["sent_time"], '%Y-%m-%d %H:%M:%S.%f')
                print( 'SENT TIME: ', sent_time)
                print( 'RECV TIME: ',datetime.now())
                tt =         datetime.now()-sent_time
                tt_seconds = tt.total_seconds()
                print( 'TRABSIT T: ',tt_seconds )
                
                print(  )
                print( ' ')
                conn.sendall(data)  # Echo back the message









def main():
    procs = []
    manager = Manager()
    evnt = manager.Event()
    m = multiprocessing.Process(target=matrix, args=( evnt, ))
    w = multiprocessing.Process(target=waveform, args=( evnt, ))
    f = multiprocessing.Process(target=fx, args=( evnt, ))    
    s = multiprocessing.Process(target=socketlisten, args=( evnt, ))        
    procs.append(m)
    procs.append(w)
    procs.append(f)
    procs.append(s)    
    m.start()
    w.start()
    f.start()
    s.start()    
      
    #set_realtime_priority( w.pid )
    for proc in procs:
        proc.join()
 


if __name__ == "__main__":
    main()