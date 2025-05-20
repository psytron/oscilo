#!/usr/bin/python
# -*- coding:utf-8 -*-

# work wired with
# https://e2e.ti.com/support/data-converters-group/data-converters/f/data-converters-forum/898004/ads1256-getting-different-readings-when-using-differential-mode-vs-common-mode-on-ads1256

import time
import ADS1256mod
import RPi.GPIO as GPIO
import random

try:
    ADC = ADS1256mod.ADS1256()
    ADC.ADS1256_init()

    
    ADC_Value = ADC.ADS1256_GetAll()
    print ("0 ADC = %lf"%(ADC_Value[0]*5.0/0x7fffff))
    print ("1 ADC = %lf"%(ADC_Value[1]*5.0/0x7fffff))
    print ("2 ADC = %lf"%(ADC_Value[2]*5.0/0x7fffff))
    print ("3 ADC = %lf"%(ADC_Value[3]*5.0/0x7fffff))
    print ("4 ADC = %lf"%(ADC_Value[4]*5.0/0x7fffff))
    print ("5 ADC = %lf"%(ADC_Value[5]*5.0/0x7fffff))
    print ("6 ADC = %lf"%(ADC_Value[6]*5.0/0x7fffff))
    #print ("7 ADC = %lf"%(ADC_Value[7]*5.0/0x7fffff))
        
    print("RND    = %d" % random.randint(0, 100))
    # This line moves the cursor up 9 lines in the console
    print ('\n')
    print ( (ADC_Value[0]*5.0/0x7fffff) )


        
except :
    GPIO.cleanup()
    print ("\r\nProgram end     ")
    exit()
