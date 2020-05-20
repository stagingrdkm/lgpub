#!/bin/sh

# make sure our window gets the focus
systemctl stop appmanager

$(dirname $0)/./dac.sh $1-verity-7218refapp 7218refapp
