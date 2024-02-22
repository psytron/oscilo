



import RPi.GPIO as GPIO
import time

# Pin configuration
# DEFAULT: 
#SW = 27  # Switch pin   
#DT = 18  # Data pin
#CLK = 17  # Clock pin



# black
CLK = 16  # Clock pin
DT = 20  # Data pin
SW = 21  # Switch pin   

# Variables
px = 0  # Initial value of px
last_CLK_state = False

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN)
GPIO.setup(CLK, GPIO.IN)

# Define event handlers for rising and falling edges of CLK and DT pins
def handle_CLK_rising(channel):
    global last_CLK_state, px
    if not last_CLK_state and GPIO.input(DT) != last_CLK_state:
        px += 1  # Increment px on clockwise rotation
    elif not last_CLK_state and GPIO.input(DT) == last_CLK_state:
        px -= 1  # Decrement px on counterclockwise rotation
    last_CLK_state = True

def handle_CLK_falling(channel):
    global last_CLK_state
    last_CLK_state = False

# Define event handler for both rising and falling edges of CLK pin
def handle_CLK_edge(channel):
    global last_CLK_state, px
    current_CLK_state = GPIO.input(CLK)
    if current_CLK_state != last_CLK_state:
        if current_CLK_state and GPIO.input(DT) != current_CLK_state:
            px += 1  # Increment px on clockwise rotation
        elif current_CLK_state and GPIO.input(DT) == current_CLK_state:
            px -= 1  # Decrement px on counterclockwise rotation
    last_CLK_state = current_CLK_state


def handle_SW_press(channel):
    # Do something when the switch is pressed
    print("Switch pressed!")


# Add event listener for CLK pin
GPIO.add_event_detect(CLK, GPIO.BOTH, callback=handle_CLK_edge)    

# Add event listeners for CLK and DT pins
#GPIO.add_event_detect(CLK, GPIO.RISING, callback=handle_CLK_rising)
#GPIO.add_event_detect(CLK, GPIO.FALLING, callback=handle_CLK_falling)


# Add event listener for SW pin (optional)
GPIO.add_event_detect(SW, GPIO.FALLING, callback=handle_SW_press)

# Main loop
try:
    while True:
        time.sleep(0.01)  # Add a small delay to avoid excessive CPU usage
        print( px )

except KeyboardInterrupt:
    # Stop event detection and clean up GPIO pins when script is interrupted
    GPIO.remove_event_detect(CLK)
    GPIO.remove_event_detect(DT)
    GPIO.remove_event_detect(SW)
    GPIO.cleanup()

    print("Exiting...")
