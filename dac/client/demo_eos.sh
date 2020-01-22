#!/bin/sh

# prevent jsapp from getting back window focus
systemctl stop jsapp

export PATH=$PATH:/tmp/client

./scripts/download.sh $1 && ./scripts/unpack.sh && ./scripts/run.sh eos
