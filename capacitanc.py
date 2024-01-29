

# 1M Ohm resistor
# Jumper wires
# wire antenna

# Connect one end of the resistor to a GPIO pin on the Raspberry Pi (let's say GPIO 4).
# Connect the other end of the resistor to the antenna (the piece of wire).
# Connect the antenna to a ground pin on the Raspberry Pi through a jumper wire.


import RPi.GPIO as GPIO
import time

sensorPin = 13

GPIO.setmode(GPIO.BCM)
print(' setting gpio: ', sensorPin )
GPIO.setup(sensorPin, GPIO.OUT)

def readCapacitance():
    GPIO.output(sensorPin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.setup(sensorPin, GPIO.IN)
    start_time = time.time()
    end_time = time.time()
    while GPIO.input(sensorPin) == GPIO.HIGH:
        end_time = time.time()
        if end_time - start_time > 1:
            return False
    return end_time - start_time

while True:
    capacitance = readCapacitance()
    if capacitance:
        print("Capacitance: ", capacitance)
    else:
        print("Timeout")
    time.sleep(0.1)