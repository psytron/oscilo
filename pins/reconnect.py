





# Connect the NTC pin to a GPIO pin on the Raspberry Pi (e.g., GPIO 17)
# Connect the DIN pin to another GPIO pin on the Raspberry Pi (e.g., GPIO 18)
# Note: GND should be connected to a ground pin on the Raspberry Pi, and 3.3V to a 3.3V power pin
import RPi.GPIO as GPIO
import time

NTC_PIN = 17  # Replace with the actual GPIO number you connected to the NTC pin
DIN_PIN = 18  # Replace with the actual GPIO number you connected to the DIN pin

# Set the pin numbering system to BCM (Broadcom SOC channel)
GPIO.setmode(GPIO.BCM)
GPIO.setup(NTC_PIN, GPIO.IN)
GPIO.setup(DIN_PIN, GPIO.IN)

try:
    while True:
        # Read NTC value
        ntc_value = GPIO.input(NTC_PIN)
        print(f"NTC Value: {ntc_value}")

        # Read DIN value
        din_value = GPIO.input(DIN_PIN)
        print(f"DIN Value: {din_value}")

        time.sleep(0.01)  # Wait for 1 second before reading again

except KeyboardInterrupt:
    pass

finally:
    # Clean up GPIO settings
    GPIO.cleanup()



# The IC with marking N18 355T W is likely a temperature sensor with digital output (NTC) and digital input (DIN).
# To connect the GPIO to it, we need to set up the NTC and DIN pins as input pins.
# We have already done this above with the lines:
# GPIO.setup(NTC_PIN, GPIO.IN)
# GPIO.setup(DIN_PIN, GPIO.IN)
# Now, we can read the values from these pins as shown above.
# If you want to do something based on the values read, you can add your code here.
# For example, if the NTC value is above a certain threshold, you might want to turn on a fan.
# You can do this by setting up another GPIO pin as an output pin, and turning it on or off based on the NTC value.
# Here is an example of how you might do this:

FAN_PIN = 27  # Replace with the actual GPIO number you connected to the fan
GPIO.setup(FAN_PIN, GPIO.OUT)

try:
    while True:
        # Read NTC value
        ntc_value = GPIO.input(NTC_PIN)
        print(f"NTC Value: {ntc_value}")

        # If the NTC value is above a certain threshold, turn on the fan
        if ntc_value > 50:  # Replace 50 with the actual threshold you want to use
            GPIO.output(FAN_PIN, GPIO.HIGH)
        else:
            GPIO.output(FAN_PIN, GPIO.LOW)

        time.sleep(1)  # Wait for 1 second before reading again

except KeyboardInterrupt:
    pass

finally:
    # Clean up GPIO settings
    GPIO.cleanup()

