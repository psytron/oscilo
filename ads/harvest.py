



#!/usr/bin/python
# -*- coding:utf-8 -*-

# work wired with
# https://e2e.ti.com/support/data-converters-group/data-converters/f/data-converters-forum/898004/ads1256-getting-different-readings-when-using-differential-mode-vs-common-mode-on-ads1256

import time

import os
print(os.getcwd())
import sys
print("Current file path for module search: ", sys.path)

print( 'about to import ADS1256mod')

import RPi.GPIO as GPIO
import random
from . import ADS1256mod

ADC = ADS1256mod.ADS1256()
ADC.ADS1256_init()

        
 
# The ADS1256 ADC module used in this code can measure voltages in the range of 0 to 5V. 
# The raw ADC readings are in the range of 0 to 8388607 (or 0x7fffff in hexadecimal), ]
# which is the maximum positive value that can be represented with 24 bits.

# 0x7fffff is hexadecimal representation of the number 8388607. 
# it's used as a divisor to normalize the ADC (Analog-to-Digital Converter) readings.
# The ADS1256 ADC module used in this code has a 24-bit resolution. 
# max positive value that can be represented with 24 bits is 2^23 - 1, 
# which equals 8388607 or 0x7fffff in hexadecimal.

def yo():
    valz = ADC.ADS1256_GetAll()
    out_arr = [ valz[0]*5.0/0x7fffff ,
                valz[1]*5.0/0x7fffff ,
                valz[2]*5.0/0x7fffff ,
                valz[3]*5.0/0x7fffff ,
                valz[4]*5.0/0x7fffff ,
                valz[5]*5.0/0x7fffff ,
                valz[6]*5.0/0x7fffff ,
                valz[7]*5.0/0x7fffff ]
    return out_arr 


def read():
    ADC_Value = ADC.ADS1256_GetAll()
    out_arr = [ valz[0]*5.0/0x7fffff ,
                valz[1]*5.0/0x7fffff ,
                valz[2]*5.0/0x7fffff ,
                valz[3]*5.0/0x7fffff ,
                valz[4]*5.0/0x7fffff ,
                valz[5]*5.0/0x7fffff ,
                valz[6]*5.0/0x7fffff ,
                valz[7]*5.0/0x7fffff ]
    return out_arr 



if __name__ == 'main':
    yo()