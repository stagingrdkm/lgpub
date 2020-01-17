#!/bin/sh
iptables -F

./scripts/download.sh && ./scripts/unpack.sh && ./scripts/run.sh eos
