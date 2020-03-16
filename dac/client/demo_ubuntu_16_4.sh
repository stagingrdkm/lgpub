#!/bin/sh

./scripts/prepare.sh && ./scripts/download.sh $1 && ./scripts/unpack.sh && ./scripts/run.sh ubuntu_16_4 
