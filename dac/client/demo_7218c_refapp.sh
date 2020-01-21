#!/bin/sh

# make sure our window gets the focus
systemctl stop appmanager

./scripts/download.sh $1 && ./scripts/unpack.sh && ./scripts/run.sh 7218refapp
