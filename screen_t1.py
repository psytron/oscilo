

# THE BLUE LED SCREEN IS AN IC1602
# i2c 1602 # 
# 32 CHaracters 2 lines 16 Characters per line 
 # 32 characters (or 32 bytes / 256 bits) at a time.
 # 16x2 character LCD display. This means it can display 32 characters at a time, with each character being 8 bits (1 byte) in size.

from RPLCD.i2c import CharLCD
from time import sleep

# Initialize the LCD using the pins
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)

# Write a string to the LCD
lcd.write_string('1234567890123456')
lcd.write_string('1234567890123456')
sleep(1)
lcd.write_string('V V V V V V V V-')
lcd.write_string('8888888888888888')
sleep(1)

lcd.write_string('0000 ')
sleep(1)
lcd.write_string('0001 ')
sleep(1)
lcd.write_string('0002 ')
sleep(1)
lcd.write_string('0003 ')
sleep(1)
lcd.write_string('0004 ')
sleep(1)
lcd.write_string('0005 ')
sleep(1)


lcd.write_string('VOLT DISPLAY ')

sleep(1 )

lcd.write_string('0007 NANOSEC NANO SEC')

sleep(1 )
lcd.write_string('VOLTS READ  ')

sleep(1 )
lcd.write_string('XV4343  VOOSDI')