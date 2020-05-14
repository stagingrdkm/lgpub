#!/bin/sh

# prevent jsapp from getting back window focus
systemctl stop jsapp

./dac.sh $1 7218
