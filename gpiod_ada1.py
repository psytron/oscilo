import gpiod

with gpiod.Chip("/dev/gpiochip4") as chip:
    info = chip.get_info()
    print(f"{info.name} [{info.label}] ({info.num_lines} lines)")