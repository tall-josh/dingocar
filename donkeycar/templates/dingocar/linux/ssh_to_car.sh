#!/bin/bash

CAR_ADDRESS="pi@your_car.local"
PORT=2050

ssh -AR $PORT:localhost:22 $CAR_ADDRESS
