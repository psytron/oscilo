import sounddevice as sd
import threading
import time
import queue

# Audio parameters
CHUNK = 1024  # Adjust buffer size as needed
SAMPLE_RATE = 44100

# Data storage and synchronization
modified_data = [0] * CHUNK  # Initial silence
data_queue = queue.Queue()
play_event = threading.Event()
stop_event = threading.Event()

def playback_thread():
    global play_event, stop_event

    with sd.OutputStream(channels=1, samplerate=SAMPLE_RATE, blocksize=CHUNK) as stream:
        while not stop_event.is_set():
            if not data_queue.empty():
                modified_data = data_queue.get()

            stream.write(modified_data)
            play_event.set()  # Signal buffer completion

            # Wait for next buffer or stop signal
            if not stop_event.is_set():
                play_event.wait()
                play_event.clear()

import numpy as np

def modification_thread():
    global data_queue
    while not stop_event.is_set():
        # Simulate generating modified audio data
        for i in range(CHUNK):
            modified_data[i] = i  # Example modification: ramp

        # Convert to float32
        modified_data = np.array(modified_data, dtype='float32')

        data_queue.put(modified_data)
        time.sleep(0.01)  # Adjust sleep time based on processing needs

# Start threads
playback_thread = threading.Thread(target=playback_thread)
modification_thread = threading.Thread(target=modification_thread)
playback_thread.start()
modification_thread.start()

# Allow time for threads to synchronize
time.sleep(0.5)

try:
    # Perform modifications during playback (simulated here)
    for i in range(10):
        print(f"Modifying data for the {i+1}th time...")
        time.sleep(1)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Stop processing and playback
    stop_event.set()
    playback_thread.join()
    modification_thread.join()

print("Done!")
