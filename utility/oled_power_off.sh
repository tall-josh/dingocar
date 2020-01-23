#!/bin/bash

# First wait a second to let the rest of the system scripts shutdown
#/bin/sleep 1

# Send i2c command to directly power off the OLED
# i2c address = 0x3C, command byte = 0x00, display off cmd = 0xAE
/usr/sbin/i2cset -y 1 0x3C 0x00 0xAE