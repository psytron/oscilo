



from pyo import *

# Start the server
s = Server().boot()

# Frequency of the tone (adjust as needed)
frequency = 440.0  # in Hertz (Hz)

# Amplitude (adjust as needed)
amplitude = 0.5

# Create a sine wave oscillator
oscillator = Sine(frequency, mul=amplitude)

# Start the oscillator
oscillator.out()

# Start the server's audio processing
s.start()

# Run for 5 seconds (adjust as needed)
s.gui(locals())
s.stop()