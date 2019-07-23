#!/bin/bash

# Helper function that will call save_tub.py (see that file for a description)
# then sends the data to a remote machine for training.

source vars.sh

MESSAGE=${1:-"-"}

# Where to fine the tub to save
TUB='tub'

echo "Making nice tub :-) "
TUBDIR=`python organize_tub.py -t ${TUB} -s ${PI_SAVEDIR} --message "${MESSAGE}" ${CLEARTUB}`

# sent to a remote machine for training if you want.
echo rync from ${TUBDIR} to:
echo ${PC_ADDRESS}:${PC_SAVEDIR}
rsync -avz -e "ssh -p 2050" ${TUBDIR} ${PC_ADDRESS}:${PC_SAVEDIR}
