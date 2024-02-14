import RPi.GPIO as GPIO
import time

# Variables
px = 0  # Initial value of px
px2 = 0
last_CLK_state = False
last_CLK_state2 = False

def handle_CLK_edge(channel):
    global last_CLK_state
    global px
    current_CLK_state = GPIO.input(CLK)
    if current_CLK_state != last_CLK_state:
        if current_CLK_state and GPIO.input(DT) != current_CLK_state:
            px += 1  # Increment px on clockwise rotation
        elif current_CLK_state and GPIO.input(DT) == current_CLK_state:
            px -= 1  # Decrement px on counterclockwise rotation
    last_CLK_state = current_CLK_state

def handle_SW_press(channel):
    print("Switch pressed!")

def handle_CLK_edge2(channel):
    global last_CLK_state2
    global px2
    current_CLK_state2 = GPIO.input(CLK2)
    if current_CLK_state2 != last_CLK_state2:
        if current_CLK_state2 and GPIO.input(DT2) != current_CLK_state2:
            px2 += 1  # Increment px on clockwise rotation
        elif current_CLK_state2 and GPIO.input(DT2) == current_CLK_state2:
            px2 -= 1  # Decrement px on counterclockwise rotation
    last_CLK_state2 = current_CLK_state2

def handle_SW_press2(channel):
    print("Switch pressed2!")       

def setup_rotary_listener( CLK = 16  , DT = 20, SW = 21 , CLK2=23 , DT2=24 , SW2=25 , callback_in=print  ):
    #CLK = 16  # Clock pin
    #DT = 20  # Data pin
    #SW = 21  # Switch pin   

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DT, GPIO.IN)
    GPIO.setup(CLK, GPIO.IN)
    
    GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DT2, GPIO.IN)
    GPIO.setup(CLK2, GPIO.IN)

    # Add event listener for CLK pin
    GPIO.add_event_detect(CLK, GPIO.BOTH, callback=handle_CLK_edge)    
    GPIO.add_event_detect(SW, GPIO.FALLING, callback=handle_SW_press)
    GPIO.add_event_detect(CLK2, GPIO.BOTH, callback=handle_CLK_edge2)    
    GPIO.add_event_detect(SW2, GPIO.FALLING, callback=handle_SW_press2)     

    try:
        while True:
            time.sleep(0.01) # CPU LIMIT
            callback_in( px , px2 )
    except KeyboardInterrupt:
        GPIO.remove_event_detect(CLK)
        GPIO.remove_event_detect(DT)
        GPIO.remove_event_detect(SW)
        GPIO.cleanup()

if __name__ == "__main__":
    def print_px_a(px , px2):
        print("A px value: ", px , px2)
    setup_rotary_listener( 16,20,21,23,24,25,print_px_a)