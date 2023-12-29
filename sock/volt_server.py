import socket
import numpy as np
import time

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
SAMPLING_RATE = 44100  # Samples per second

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f'Connected by {addr}')
        while True:
            # Generate sine wave data
            t = time.time()
            samples = np.sin(2 * np.pi * 440 * t * np.arange(SAMPLING_RATE) / SAMPLING_RATE)
            data = samples.astype(np.float32).tobytes()

            # Send the wave data
            conn.sendall(data)
