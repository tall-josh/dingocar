#!/usr/bin/env python3

# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import time

# UMU library
import GY91

# MCP3021 is DingoCar PCB battery voltage ADC on I2C bus
def get_battery_voltage():
    MCP3021_I2CADDR = 0x4d  # default address
    MCP3021_RATIO = 0.0169  # to times ADC value to conv to voltage based on our voltage divider

    adc_val = i2cbus.read_word_data(MCP3021_I2CADDR, 0)

    # from this data we need the last 4 bits and the first 6.
    last_4 = adc_val & 0b1111  # using a bit mask
    first_6 = adc_val >> 10  # left shift 10 because data is 16 bits

    # together they make the voltage conversion ratio
    # to make it all easier the last_4 bits are most significant :S
    vratio = last_4 << 6 | first_6

    return round(vratio * MCP3021_RATIO, 2)

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

disp.begin()
disp.clear()
disp.display()

# Access the same i2c bus that the Adafruit lib uses 
i2cbus = disp._i2c._bus

# Now have i2c bus, initialise the GY91 module
gy91 = GY91.GY91(bus=i2cbus)

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

# Can display multiple pages, which one to display
currentPage = 0 # select which page/group of info to display
framesDisplayed = 0 # increment each time we do an update

while True:
    # Setup and draw for every page type
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    battery = get_battery_voltage()
    draw.text((x, top),       "DingoCar",  font=font, fill=255)
    draw.text((x, top+8),     "Battery:" + str(battery),  font=font, fill=255)

    if currentPage == 0:

        # Main page

        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True ).decode('utf-8')
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True ).decode('utf-8')      
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True ).decode('utf-8')      
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell = True ).decode('utf-8') 

        draw.text((x, top+16),    "IP: " + str(IP),  font=font, fill=255)
        draw.text((x, top+40),    str(CPU), font=font, fill=255)
        draw.text((x, top+48),    str(MemUsage),  font=font, fill=255)
        draw.text((x, top+56),    str(Disk),  font=font, fill=255)

        if framesDisplayed > 1:
            # Delay before next frame
            time.sleep(1)

        # See if we go to next page
        if framesDisplayed > 3:
            currentPage = 1
            framesDisplayed = 0

    elif currentPage == 1:

        # IMU page

        # read sensor values
        accel = gy91.readAccel()
        gyro = gy91.readGyro()
        mag = gy91.readMagnet()
        temp1 = round(gy91.readTemperature(),1)
        temperature,pressure,humidity = gy91.readBME280All()

        # display them

        draw.text((x, top+16),    "ax: " + str(accel['x']),  font=font, fill=255)
        draw.text((x, top+24),    "ay: " + str(accel['y']),  font=font, fill=255)
        draw.text((x, top+32),    "az: " + str(accel['z']),  font=font, fill=255)

        draw.text((x, top+40),    "gx: " + str(gyro['x']),  font=font, fill=255)
        draw.text((x, top+48),    "gy: " + str(gyro['y']),  font=font, fill=255)
        draw.text((x, top+56),    "gz: " + str(gyro['z']),  font=font, fill=255)

        draw.text((x+64, top+40),    "mx: " + str(mag['x']),  font=font, fill=255)
        draw.text((x+64, top+48),    "my: " + str(mag['y']),  font=font, fill=255)
        draw.text((x+64, top+56),    "mz: " + str(mag['z']),  font=font, fill=255)

        #draw.text((x+64, top+16),    "T1: " + str(temp1),  font=font, fill=255)
        draw.text((x+64, top+16),    "T: " + str(temperature) + "C",  font=font, fill=255)
        draw.text((x+64, top+24),    "P: " + str(pressure) + "hPa",  font=font, fill=255)
        draw.text((x+64, top+32),    "H: " + str(humidity) + "%",  font=font, fill=255)

        # See if we go to next page
        if framesDisplayed > 30:
            currentPage = 0
            framesDisplayed = 0

        time.sleep(0.1)

    # Now display whats been presented
    image_rotated = image.rotate(180)
    disp.image(image_rotated)
    disp.display()
    framesDisplayed += 1

