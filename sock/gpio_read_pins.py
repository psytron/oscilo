


import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
ntc_pin = 17  # Replace with the actual GPIO number you connected to the NTC pin
din_pin = 18  # Replace with the actual GPIO number you connected to the DIN pin

# Set up GPIO pin modes
GPIO.setup(ntc_pin, GPIO.IN)
GPIO.setup(din_pin, GPIO.IN)

try:
    while True:
        # Read NTC value
        ntc_value = GPIO.input(ntc_pin)
        print(f"NTC Value: {ntc_value}")

        # Read DIN value
        din_value = GPIO.input(din_pin)
        print(f"DIN Value: {din_value}")

        time.sleep(1)  # Wait for 1 second before reading again

except KeyboardInterrupt:
    pass

finally:
    # Clean up GPIO settings
    GPIO.cleanup()