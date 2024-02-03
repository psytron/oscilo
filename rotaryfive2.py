
import gpiod
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

    chip = gpiod.Chip('/dev/gpiochip4')
    
    CLK_line = chip.get_line(CLK)
    DT_line = chip.get_line(DT)
    SW_line = chip.get_line(SW)

    # Requesting access to the CLK line for both rising and falling edge events
    # 'consumer' is the name of the program requesting access
    # 'type' specifies the type of event to listen for
    CLK_line.request(consumer='my_app', type=gpiod.LINE_REQ_EV_BOTH_EDGES)
    DT_line.request(consumer='my_app', type=gpiod.LINE_REQ_DIR_IN)
    SW_line.request(consumer='my_app', type=gpiod.LINE_REQ_EV_FALLING_EDGE)

    def handle_CLK_edge(event_line):
        nonlocal last_CLK_state
        nonlocal px
        current_CLK_state = event_line.event_read()
        if current_CLK_state != last_CLK_state:
            if current_CLK_state and DT_line.get_value() != current_CLK_state:
                px += 1  # Increment px on clockwise rotation
            elif current_CLK_state and DT_line.get_value() == current_CLK_state:
                px -= 1  # Decrement px on counterclockwise rotation
        last_CLK_state = current_CLK_state

    def handle_SW_press(event_line):
        print("Switch pressed!")

    try:
        while True:
            time.sleep(0.01) # CPU LIMIT
            callback_in( px )
            CLK_line.event_wait(sec=0)
            handle_CLK_edge(CLK_line)
            SW_line.event_wait(sec=0)
            handle_SW_press(SW_line)
    except KeyboardInterrupt:
        CLK_line.release()
        DT_line.release()
        SW_line.release()
        chip.close()



def value_updated(value):
    print("Value updated: ", value)

if __name__ == "__main__":
    setup_rotary_listener(value_updated)
