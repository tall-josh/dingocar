#!/bin/bash

##################################################
# COMMON VARIABLES
##################################################
PC_USER=rick-sanchez
PC_ADDRESS=${PC_USER}@localhost

# Where to save the cleaned to in a more perminant
# location on your pc.
PC_SAVEDIR=/perminant/place/on/pc/to/store/tubs
PC_MODELDIR=/perminant/place/on/pc/to/store/models


##################################################
# CAR VARIABLES
##################################################
# Where to save the 'cleaned' tub on the pi 
# (just incase something goes wrong in during
# the rsync)
CAR_SAVEDIR=/temp/place/on/pi/to/store/tubs
CAR_MODELDIR=/place/on/pi/you/want/to/store/models

# Keep or delete all but 'meta.json' from TUB when complete 
#CLEARTUB=""
CLEARTUB="--clear-tub"


##################################################
# PC VARIABLES
##################################################
CAR_USER=pi
CAR_NAME=raspberry
CAR_ADDRESS=${CAR_USER}@${CAR_NAME}.local
