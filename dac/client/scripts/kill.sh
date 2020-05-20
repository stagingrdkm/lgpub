#!/bin/sh

user=$(whoami)
sudo=""
if [ "$user" != "root" ]; then
    sudo="sudo "
fi

$sudo killall -9 wayland-egl-test wayland-egl-test-input runc crun flutter-launcher-wayland Auryn
sleep 2

if [ -f /usr/bin/crun ]; then
  crun kill -a test
  crun delete test
else
  runc kill -a test
  runc delete test
fi

if [ -f rootfs.sqsh.verity ]; then
  echo Detected verity image!
  ${DAC_ROOT}scripts/verity_umount.sh
fi
