

SAMPLING_RATE = 44100

import socket
import numpy as np
import matplotlib.pyplot as plt

HOST = 'localhost'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(-1.1, 1.1)
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Amplitude')
ax.set_title('Received Sine Wave')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = b''
    while True:
        # Receive wave data in chunks
        chunk = s.recv(4096)  # Adjust chunk size as needed
        print('  - ', chunk )
        if not chunk:
            break
        data += chunk

        # Process and visualize the received data
        samples = np.frombuffer(data, dtype=np.float32)
        time_axis = np.linspace(0, len(samples) / SAMPLING_RATE, len(samples))
        line.set_data(time_axis, samples)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Clear the data for the next chunk
        data = b''
