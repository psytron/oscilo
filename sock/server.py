


import socket
from datetime import datetime
            

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
            data = conn.recv(1024)
            if not data:
                break
            print(f'Received: {data.decode()}')
            print( 'MACHINE : ',datetime.now())
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



