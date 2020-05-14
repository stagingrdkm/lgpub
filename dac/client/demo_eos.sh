#!/bin/sh

# prevent jsapp from getting back window focus
systemctl stop jsapp

export PATH=$PATH:/tmp/client

./dac.sh $1 eos
