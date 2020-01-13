#!/bin/sh
#
# Activate the Python environment, then run a Python script

SCRIPT=$1
PARAMETER=$2

. $HOME/env/bin/activate
./$SCRIPT $PARAMETER
