from signalflow import *

#--------------------------------------------------------------------------------
# An AudioGraph is made up of a network of interconnected Nodes, which generate
# and process audio. 
#--------------------------------------------------------------------------------
graph = AudioGraph()

#--------------------------------------------------------------------------------
# Passing an array of frequencies creates a stereo output.
#--------------------------------------------------------------------------------
import pyautogui

# Get the screen size
screen_width, screen_height = pyautogui.size()

# Function to map mouse y position to frequency
def map_mouse_to_freq(mouse_y, freq_min=264, freq_max=528):
    return ((freq_max - freq_min) * (mouse_y / screen_height)) + freq_min

# Get the current mouse position
mouse_x, mouse_y = pyautogui.position()

# Map the mouse y position to a frequency
freq = map_mouse_to_freq(mouse_y)

sine = SineOscillator([freq, freq * 2])


#--------------------------------------------------------------------------------
# Simple attack/sustain/release envelope with linear curves.
#--------------------------------------------------------------------------------
env = ASREnvelope(0.1, 0.5, 0.5)

#--------------------------------------------------------------------------------
# Use standard arithmetic operations to combine signals. When a multi-channel 
# signal is multiplied by a mono signal, the mono signal is auto-upmixed.
#--------------------------------------------------------------------------------
output = sine * env

#--------------------------------------------------------------------------------
# Connect the output to the graph, and begin playback.
#--------------------------------------------------------------------------------
output.play()


while True:
    # Get the current mouse position
    mouse_x, mouse_y = pyautogui.position()

    # Map the mouse y position to a frequency
    freq = map_mouse_to_freq(mouse_y)

    print( freq , mouse_x , mouse_y , sine  )


graph.wait()