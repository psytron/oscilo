

from RPLCD.i2c import CharLCD
from time import sleep

# Initialize the LCD using the pins
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)

# Write a string to the LCD
lcd.write_string('VOLT DISPLAY ')

sleep(1 )

lcd.write_string('VOLTS READ  ')