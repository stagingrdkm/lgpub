#!/bin/sh

sudo killall -9 wayland-egl-test wayland-egl-test-input runc crun flutter-launcher-wayland Auryn
sleep 2

runc kill -a test
runc delete test
crun kill -a test
crun delete test

if [ -f rootfs.sqsh.verity ]; then
  echo Detected verity image!
  ./scripts/verity_umount.sh
fi
