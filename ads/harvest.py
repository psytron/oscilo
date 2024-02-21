



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

import socket
import datetime

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



def stream_to_address_on_port( address_in , port_in ):
    HOST = address_in
    PORT = port_in
    # Create a socket object using socket.socket() method
    # AF_INET is the address family of the socket. This is the Internet address family for IPv4.
    # SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport our messages in the network.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            message = read()
            
            # override to send timestamp 
            # message = str(datetime.datetime.now())
            
            s.sendall(message.encode())
            
            data = s.recv(1024)
            print(f'Received: {data.decode()}')




if __name__ == 'main':
    yo()