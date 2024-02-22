


import socket
from datetime import datetime
import json
            

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






            # Known audio frequencies and their emotional or psychological effects:
            # 440 Hz - Standard tuning frequency, balanced, stable
            # 432 Hz - Natural tuning frequency, calming, healing
            # 528 Hz - Love frequency, transformation, miracles
            # 639 Hz - Connecting/relationships, tolerance, love
            # 852 Hz - Awakening intuition, returning to spiritual order

            # 396 Hz - Liberating guilt and fear
            # 417 Hz - Undoing situations and facilitating change
            # 741 Hz - Awakening intuition, solving problems
            # 963 Hz - Awakening perfect state, returning to oneness




note_freq_map = {
    'A4': 440.00,
    'B4': 493.88,
    'C4': 261.63,
    'D4': 293.66,
    'E4': 329.63,
    'F4': 349.23,
    'G4': 392.00,
    'A5': 880.00,
    'B5': 987.77,
    'C5': 523.25,
    'D5': 587.33,
    'E5': 659.25,
    'F5': 698.46,
    'G5': 783.99
}


# first define range of musical notes 
# constrain based on harmonics / scales 
# learn native voltage range including 0 and max 
# loop and test delta , if delta  = 0 do nothing 
# + delta magnitude = walk up from last note 
# - delta magnitude = walk down from last note 



