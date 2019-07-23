#!/bin/bash

PI_USER=pi
PI_NAME=raspberry
PI_ADDRESS=${PI_USER}@${PI_NAME}.local

# Where to save the 'cleaned' tub on the pi 
# (just incase something goes wrong in during
# the rsync)
PI_SAVEDIR=/temp/place/on/pi/to/store/tubs

PI_MODEL=/place/on/pi/you/want/to/store/models

# Keep or delete all but 'meta.json' from TUB when complete 
#CLEARTUB=""
CLEARTUB="--clear-tub"

PC_USER=rick-sanchez
PC_ADDRESS=${PC_USER}@localhost

# Where to save the cleaned to in a more perminant
# location on your pc.
PC_SAVEDIR=/perminant/place/on/pc/to/store/tubs

