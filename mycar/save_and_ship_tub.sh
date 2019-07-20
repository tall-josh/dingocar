#!/bin/bash

# Helper function that will call save_tub.py (see that file for a description)
# then sends the data to a remote machine for training.

MESSAGE=${1:-"-"}

# Where to save the 'clearned' tub on the pi 
# (just incase something goes wrong in during
# the rsync)
SAVEDIR="/home/users/josh/repos/mine/data/ZZZ_DEBUG"

# Where to fine the tub to save
TUB='tub'

# Keep or delete all but 'meta.json' from TUB when complete 
#CLEARTUB=""
CLEARTUB="--clear-tub"

echo "Making nice tub :-) "
TUBDIR=`python save_tub.py -t $TUB -s $SAVEDIR --message "$MESSAGE" $CLEARTUB`

# 
LOCAL_MACHINE="jp@localhost"
SAVEDIR="/home/jp/Documents/repos/donkeycar/data/"

# sent to a remote machine for training if you want.
echo rync from ${TUBDIR} to:
echo $LOCAL_MACHINE:$SAVEDIR
rsync -avz -e "ssh -p 2050" $TUBDIR $LOCAL_MACHINE:$SAVEDIR
