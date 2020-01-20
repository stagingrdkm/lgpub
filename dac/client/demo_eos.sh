#!/bin/sh
iptables -F

./scripts/download.sh $1 && ./scripts/unpack.sh && ./scripts/run.sh eos
