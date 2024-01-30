
# 1M Ohm resistor
# Jumper wires
# wire antenna

# Connect one end of the resistor to a GPIO pin on the Raspberry Pi (let's say GPIO 13).
# Connect the other end of the resistor to the antenna (the piece of wire).
# Connect the antenna to a ground pin on the Raspberry Pi through a jumper wire.

# This script is used to measure the capacitance of a circuit using a Raspberry Pi.
# The circuit consists of a 1M Ohm resistor, jumper wires, and a wire antenna.
# The resistor is connected to a GPIO pin on the Raspberry Pi (in this case, GPIO 13).
# The other end of the resistor is connected to the antenna (the piece of wire).
# The antenna is then connected to a ground pin on the Raspberry Pi through a jumper wire.
# 
# The script works by setting the GPIO pin to output and sending a HIGH signal.
# It then switches the GPIO pin to input and measures the time it takes for the pin to read LOW.
# This time is directly proportional to the capacitance of the circuit.
# The higher the capacitance, the longer it will take for the pin to read LOW.
# 
# The script continuously reads the capacitance and prints the value.
# If the reading takes more than 1 second, it assumes that the circuit is open (infinite capacitance) and prints "Timeout".

import RPi.GPIO as GPIO
import time

sensorPin = 13

GPIO.setmode(GPIO.BCM)
print(' setting gpio: ', sensorPin )
GPIO.setup(sensorPin, GPIO.OUT)

def readCapacitance():
    GPIO.setup(sensorPin, GPIO.OUT)
    GPIO.output(sensorPin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.setup(sensorPin, GPIO.IN)
    start_time = time.time()
    end_time = time.time()
    while GPIO.input(sensorPin) == GPIO.HIGH:
        end_time = time.time()
        if end_time - start_time > 1:
            return False
    GPIO.setup(sensorPin, GPIO.OUT)  # Set the sensorPin as an output again before the function ends
    return end_time - start_time

while True:
    capacitance = readCapacitance()
    if capacitance:
        print("Capacitance: ", capacitance)
    else:
        print("Timeout")
    