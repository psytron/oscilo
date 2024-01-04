


import time
import RPi.GPIO as GPIO

# Use the Broadcom SOC channel
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin you've connected to
input_pin = 4

# Set the pin to input mode
GPIO.setup(input_pin, GPIO.IN)

try:
    while True:
        # Read the sensor value
        sensor_value = GPIO.input(input_pin)

        # Print the sensor value
        print("Sensor value: ", sensor_value)

        # Wait for a second before reading the sensor again
        time.sleep(1)

except KeyboardInterrupt:
    # Reset GPIO settings if the script is exited with CTRL+C
    GPIO.cleanup()