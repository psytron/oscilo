

from gpiozero import DigitalInputDevice, DigitalOutputDevice
from time import sleep

output_device = DigitalOutputDevice( 26 )

while True:
    output_device.on()
    sleep(1)
    output_device.off()
    sleep(1)
