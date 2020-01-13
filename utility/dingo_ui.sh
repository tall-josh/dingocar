#!/bin/sh

MESSAGE=$1

. $HOME/env/bin/activate
./dingo_ui.py $MESSAGE
