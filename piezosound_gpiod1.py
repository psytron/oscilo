
# Connect one terminal of the piezoelectric buzzer to a GPIO pin on the Raspberry Pi (let's say GPIO 18).
# Connect the other terminal of the buzzer to a ground pin on the Raspberry Pi.
# The following script will generate different frequencies of sound using numpy and send it to the piezoelectric buzzer.

import gpiod
import time
import numpy as np

buzzerPin = 26
chip = gpiod.Chip('gpiochip4')
line = chip.get_line(buzzerPin)
line.request(consumer='my_app', type=gpiod.LINE_REQ_DIR_OUT)

try:
    line.set_value(1)
    time.sleep(1)
    line.set_value(0)
    time.sleep(1)
    line.set_value(1)
    time.sleep(1)

finally:
    line.release()
