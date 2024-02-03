import gpiod
from gpiod.line import Direction, Value, Event

CLK = 16  # Clock pin
DT = 20  # Data pin
SW = 21  # Switch pin   

#i3

chip = gpiod.Chip('/dev/gpiochip4')

# Request lines
lines = chip.get_lines([CLK, DT, SW])
lines.request(consumer="blink-example", type=gpiod.LINE_REQ_EV_BOTH_EDGES)

# Initial state
last_CLK_state = lines[0].event_read().event_type

def event_callback(line):
    global last_CLK_state
    event = line.event_read()
    current_CLK_state = event.event_type
    current_DT_state = lines[1].get_value()

    if current_CLK_state != last_CLK_state:  # Means the knob is rotating
        # if the DT state is different than the CLK state, that means the knob is rotating clockwise (right)
        if current_DT_state != current_CLK_state:
            print("+1")
        else:
            print("-1")  # else it's rotating counterclockwise (left)

    last_CLK_state = current_CLK_state  # Update the last CLK state

# Register event callback
lines[0].event_wait(sec=0)
lines[0].event_config(type=gpiod.LINE_REQ_EV_BOTH_EDGES, callback=event_callback)

while True:
    time.sleep(0.1)  # CPU LIMIT