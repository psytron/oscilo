



#!/usr/bin/python
# -*- coding:utf-8 -*-

# work wired with
# https://e2e.ti.com/support/data-converters-group/data-converters/f/data-converters-forum/898004/ads1256-getting-different-readings-when-using-differential-mode-vs-common-mode-on-ads1256

import time
from ads1256 import ADS1256
import RPi.GPIO as GPIO
import random


try:
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()

    while(1):
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
        print ("\33[9A")

        
except :
    GPIO.cleanup()
    print ("\r\nProgram end     ")
    exit()



def read():
    out_arr =[]
    ADC_Value = ADC.ADS1256_GetAll()
    out_arr[0] = ADC_Value[0]*5.0/0x7fffff
    out_arr[1] = ADC_Value[1]*5.0/0x7fffff
    out_arr[2] = ADC_Value[2]*5.0/0x7fffff
    out_arr[3] = ADC_Value[3]*5.0/0x7fffff
    out_arr[4] = ADC_Value[4]*5.0/0x7fffff
    out_arr[5] = ADC_Value[5]*5.0/0x7fffff
    out_arr[6] = ADC_Value[6]*5.0/0x7fffff
    return out_arr 