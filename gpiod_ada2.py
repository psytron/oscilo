import time
import gpiod
from gpiod.line import Direction, Value
import numpy as np

LINE = 26

delay = 0.001

with gpiod.request_lines(
    "/dev/gpiochip4",
    consumer="blink-example",
    config={
        LINE: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        )
    },
) as request:
    start_time = time.time()
    while True:
        
        elapsed_time = time.time() - start_time
        delay = 0.0001 + (0.1 - 0.0001) * (np.sin(elapsed_time) + 1) / 2
        request.set_value(LINE, Value.ACTIVE)
        time.sleep(delay)
        request.set_value(LINE, Value.INACTIVE)
        time.sleep(delay)
