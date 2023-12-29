



import fluidsynth
import multiprocessing
import time

def fluidsynth_process():
    # Initialize FluidSynth
    fs = fluidsynth.Synth()
    fs.start(driver="coreaudio")

    # Load a SoundFont file
    sfid = fs.sfload("ZFont.sf2")

    # Set the SoundFont for the default channel
    fs.program_select(0, sfid, 0, 0)

    # Create a pipe for communication between processes
    # Create a bidirectional communication channel between two processes
    # The Pipe() function returns a pair of connection objects connected by a pipe
    # The two connection objects returned represent two ends of the pipe
    # Each connection object has send() and recv() methods (among others)
    # Here, parent_conn is used in the main process to send and receive messages
    # And child_conn is used in the child process (created later) to receive and send messages
    parent_conn, child_conn = multiprocessing.Pipe()

    # Start a separate process to listen for notes and play them in FluidSynth
    note_process = multiprocessing.Process(target=note_listener, args=(fs, child_conn))
    note_process.start()

    # Enter a loop in the main process (just for demonstration purposes)
    try:
        while True:
            # Trigger a note (replace with your logic)
            note = 60  # MIDI note number (e.g., middle C)
            velocity = 80  # Note velocity

            # Send the note information to the other process
            parent_conn.send((note, velocity))

            time.sleep(1)  # Sleep for demonstration purposes
    except KeyboardInterrupt:
        pass
    finally:
        # Close the connection and stop FluidSynth
        parent_conn.close()
        fs.delete()

def note_listener(fluidsynth_instance, conn):
    # Continuously listen for note information and play notes in FluidSynth
    try:
        while True:
            # Receive note information from the main process
            note, velocity = conn.recv()

            # Play the note in FluidSynth
            fluidsynth_instance.noteon(0, note, velocity)

            # Sleep for a short duration (adjust as needed)
            time.sleep(0.1)

            # Stop the note after a short duration (adjust as needed)
            fluidsynth_instance.noteoff(0, note)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop FluidSynth when the note listener process is terminated
        fluidsynth_instance.delete()

if __name__ == "__main__":
    fluidsynth_process()
