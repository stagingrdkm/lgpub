#!/bin/sh

# make sure our window gets the focus
systemctl stop appmanager

./dac.sh $1 rpi
