#!/bin/sh

# prevent jsapp from getting back window focus
systemctl stop jsapp

$(dirname $0)/./dac.sh $1 7218
