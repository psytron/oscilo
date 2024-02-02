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
        request.set_value(LINE, Value.ACTIVE)
        time.sleep( delay )
        request.set_value(LINE, Value.INACTIVE)
        time.sleep( delay )
        
        elapsed_time = time.time() - start_time
        delay = 0.05 * (1 + np.sin(2 * np.pi * elapsed_time / 10))
        request.set_value(LINE, Value.ACTIVE)
        time.sleep(delay)
        request.set_value(LINE, Value.INACTIVE)
        time.sleep(delay)
