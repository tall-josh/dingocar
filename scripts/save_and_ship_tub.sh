#!/bin/bash

# Helper function that will call save_tub.py (see that file for a description)
# then sends the data to a remote machine for training.

MESSAGE=${1:-"-"}

# Where to save the 'clearned' tub on the pi 
# (just incase something goes wrong in during
# the rsync)
SAVEDIR="/home/users/crocodile-dundee/dingodata/"

# Where to fine the tub to save
TUB='tub'

# Keep or delete all but 'meta.json' from TUB when complete 
#CLEARTUB=""
CLEARTUB="--clear-tub"

echo "Making nice tub :-) "
TUBDIR=`python save_tub.py -t $TUB -s $SAVEDIR --message "$MESSAGE" $CLEARTUB`

# Where to save the tub back on your local machine
LOCAL_MACHINE="dundee@localhost"
SAVEDIR="/home/dundee/Documents/repos/dingocar/data/"

# Sent to a remote machine for training if you want.
echo rync from ${TUBDIR} to:
echo $LOCAL_MACHINE:$SAVEDIR
rsync -avz -e "ssh -p 2050" $TUBDIR $LOCAL_MACHINE:$SAVEDIR
