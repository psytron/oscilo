

import RPi.GPIO as GPIO


DIN_PIN = 17  # Digital input pin
NTC_PIN = 18  # Analog input pin

# Set the pin numbering system to BCM (Broadcom SOC channel)
# BCM stands for Broadcom SOC channel, it means that we are referring to the pins by the "Broadcom SOC channel" number,
# these are the numbers after "GPIO" in the green boxes around the outside of the below diagrams.
GPIO.setmode(GPIO.BCM)
GPIO.setup(NTC_PIN, GPIO.IN)
GPIO.setup(DIN_PIN, GPIO.IN)

while True:
    ntc_value = GPIO.input(NTC_PIN)  # Read analog value
    din_value = GPIO.input(DIN_PIN)  # Read digital value

    # Process or store the data as needed
    print(f"NTC value: {ntc_value}, DIN value: {din_value}")
