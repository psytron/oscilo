



import gpiod

chip = gpiod.Chip('gpiochip4', gpiod.Chip.OPEN_BY_NAME)
line = chip.get_line(18)
line.request(consumer="blinktest", type=gpiod.LINE_REQ_DIR_OUT)

while True:
    line.set_value(1)
    line.set_value(0)