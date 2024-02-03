
import gpiod
from gpiod.line import Direction, Value
import time
 

CLK = 16  # Clock pin
DT = 20  # Data pin
SW = 21  # Switch pin   

# Variables
px = 0  # Initial value of px
last_CLK_state = False

chip = gpiod.Chip('/dev/gpiochip4')
rqLines = gpiod.request_lines( "/dev/gpiochip4",consumer="blink-example",
    config={
        CLK: gpiod.LineSettings(direction=Direction.INPUT, output_value=Value.ACTIVE),
        DT: gpiod.LineSettings(direction=Direction.INPUT, output_value=Value.ACTIVE),
        SW: gpiod.LineSettings(direction=Direction.INPUT, output_value=Value.ACTIVE),

})


last_CLK_state= rqLines.get_values()[0].value

while True:
    time.sleep(0.1) # CPU LIMIT
    valz =  rqLines.get_values()

    current_CLK_state = valz[0].value
    current_DT_state = valz[1].value

    if current_CLK_state != last_CLK_state:  # Means the knob is rotating
        # if the DT state is different than the CLK state, that means the knob is rotating clockwise (right)
        if current_DT_state != current_CLK_state:
            print("+1")
        else:
            print("-1")  # else it's rotating counterclockwise (left)

    last_CLK_state = current_CLK_state  # Update the last CLK state

