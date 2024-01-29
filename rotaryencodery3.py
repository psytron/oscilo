



import RPi.GPIO as GPIO
import time

# Pin configuration
# DEFAULT: 
#SW = 27  # Switch pin   
#DT = 18  # Data pin
#CLK = 17  # Clock pin


def setup_rotary_listener( callback_in ):
    # black
    CLK = 16  # Clock pin
    DT = 20  # Data pin
    SW = 21  # Switch pin   

    # Variables
    px = 0  # Initial value of px
    last_CLK_state = False


    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DT, GPIO.IN)
    GPIO.setup(CLK, GPIO.IN)

    def handle_CLK_edge(channel):
        nonlocal last_CLK_state
        current_CLK_state = GPIO.input(CLK)
        if current_CLK_state != last_CLK_state:
            if current_CLK_state and GPIO.input(DT) != current_CLK_state:
                px += 1  # Increment px on clockwise rotation
            elif current_CLK_state and GPIO.input(DT) == current_CLK_state:
                px -= 1  # Decrement px on counterclockwise rotation
        last_CLK_state = current_CLK_state


    def handle_SW_press(channel):
        print("Switch pressed!")


    # Add event listener for CLK pin
    GPIO.add_event_detect(CLK, GPIO.BOTH, callback=handle_CLK_edge)    
    GPIO.add_event_detect(SW, GPIO.FALLING, callback=handle_SW_press)


    try:
        while True:
            time.sleep(0.01) # CPU LIMIT
            callback_in( px )
    except KeyboardInterrupt:
        GPIO.remove_event_detect(CLK)
        GPIO.remove_event_detect(DT)
        GPIO.remove_event_detect(SW)
        GPIO.cleanup()
