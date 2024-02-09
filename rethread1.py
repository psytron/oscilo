import pyaudio
import threading
import time

CHUNK = 1024  # Adjust buffer size as needed

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)

buffers = [bytearray(CHUNK) for _ in range(2)]  # Create multiple buffers
current_buffer = 0

def playback_thread():
    global current_buffer
    while True:
        stream.write(buffers[current_buffer])
        current_buffer = (current_buffer + 1) % 2  # Switch buffers

playback_thread = threading.Thread(target=playback_thread)
playback_thread.start()

while True:
    # Modify audio data in the buffer not currently being played
    buffers[current_buffer][:] = generate_audio_data()

    time.sleep(0.01)  # Adjust sleep time based on processing need