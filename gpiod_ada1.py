import time
import gpiod
from gpiod.line import Direction, Value

LINE = 26

with gpiod.request_lines(
    "/dev/gpiochip4",
    consumer="blink-example",
    config={
        LINE: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        )
    },
) as request:
    while True:
        request.set_value(LINE, Value.ACTIVE)
        time.sleep(0.01)
        request.set_value(LINE, Value.INACTIVE)
        time.sleep(0.01)