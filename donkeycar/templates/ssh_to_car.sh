#!/bin/bash

source vars.sh

ssh -AR 2050:localhost:22 $CAR_ADDRESS
