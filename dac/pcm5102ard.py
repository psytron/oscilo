# 

# PCM5102 VCC to Raspberry Pi 3.3V
# PCM5102 GND to Raspberry Pi GND
# PCM5102 FLT to Raspberry Pi GND (for a slow roll-off filter)
# PCM5102 DMP to Raspberry Pi GND (for de-emphasis filter disabled)
# PCM5102 SCL to Raspberry Pi SCLK (GPIO 11)
# PCM5102 BCK to Raspberry Pi PCM_CLK (GPIO 18)
# PCM5102 DIN to Raspberry Pi PCM_DOUT (GPIO 21)
# PCM5102 FMT to Raspberry Pi GND (for I2S format)
# PCM5102 XSMT to Raspberry Pi GND (for soft mute disabled)
# PCM5102 SCKI to Raspberry Pi GND (for 384kHz system clock)
# PCM5102 MUTE to Raspberry Pi GND (for mute disabled)

#dtoverlay stands for Device Tree Overlay. Device Tree is a data structure 
#for describing hardware, and overlays are a way to modify the Device Tree 
#for the purpose of enabling, disabling, or configuring hardware peripherals and features.

#In this case, hifiberry-dac is the name of the overlay. 
#HiFiBerry DAC is a high-quality digital-to-analog converter for the Raspberry Pi. '
#This overlay enables the Raspberry Pi to communicate with and control the HiFiBerry DAC hardware.

#/boot/config.txt:
 #  dtoverlay=hifiberry-dac

# Please note that the device name 'hw:CARD=sndrpii2sDAC,DEV=0' 
# might be different on your system. You can list all devices by running 
# sd.query_devices() in your Python script.

import numpy as np
import sounddevice as sd

# Constants
fs = 44100  # Sample rate
f = 440    #  The frequency of the signal

# Generate the time values for one second of sound
t = np.arange(fs) / fs

# Generate a sine wave of frequency f
x = 0.5 * np.sin(2 * np.pi * f * t)

# Play the waveform out the I2S interface
sd.play(x, samplerate=fs, device='hw:CARD=sndrpii2sDAC,DEV=0')
sd.wait()