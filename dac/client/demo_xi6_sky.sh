#!/bin/sh

# make sure our window gets the focus
systemctl stop sky-appsservice

# Can't copy into /usr/bin due to readonly fs, so add the copied jq binary to the path
export PATH=$PATH:/tmp/client

# Bring up a wayland display on the host to use (since Sky westeros socket names are randomly
# generated so cannot assume which one already exists)
echo "Starting westeros display (/tmp/westeros-dac)"
export XDG_RUNTIME_DIR=/tmp
pkill "westeros"
rm /tmp/westeros-dac
rm /tmp/westeros-dac.lock
westeros --renderer /usr/lib/libwesteros_render_gl.so.0.0.0 --display westeros-dac &> /dev/null &

./scripts/prepare.sh && ./scripts/download.sh $1 && ./scripts/unpack.sh && ./scripts/run.sh xi6
