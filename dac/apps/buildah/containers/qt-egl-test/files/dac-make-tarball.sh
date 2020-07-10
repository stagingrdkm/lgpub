#!/bin/bash -ex
#
# A sample script to create a tarball for container using opkg
#
# Version: 1.0
# Author: Damian Wrobel <dwrobel@ertelnet.rybnik.pl>
#

pkg() {
  /data/dwrobel1/onemw/onemw/oe-builds/7218c-onemw-full-zb-c-2.2-flutter-gdb/onemw/build-brcm972180hbc-refboard/tmp/sysroots/x86_64-linux/usr/bin/opkg \
    --volatile-cache \
    -f /data/dwrobel1/onemw/onemw/oe-builds/7218c-onemw-full-zb-c-2.2-flutter-gdb/onemw/build-brcm972180hbc-refboard/tmp/work/7218c_debug-rdk-linux-gnueabi/core-image-efl-nodejs/1.0-r0/opkg.conf \
    -t /data/dwrobel1/onemw/onemw/oe-builds/7218c-onemw-full-zb-c-2.2-flutter-gdb/onemw/build-brcm972180hbc-refboard/tmp/work/7218c_debug-rdk-linux-gnueabi/core-image-efl-nodejs/1.0-r0/temp/ipktemp/ \
    -o $PWD/rootfs  --prefer-arch-to-version "$@"
}

rm -rf rootfs
mkdir rootfs

pkg update
pkg install qt-egl-test busybox
pkg remove --force-depends wayland-egl

pushd rootfs
rm -rf usr/libv3d* usr/lib/libEGL* usr/lib/libGLES* usr/lib/libnexus* usr/lib/libnxclient* usr/lib/libnxpl* usr/lib/libv3d* usr/lib/libwayland-server* usr/lib/libwidevine* usr/lib/libplayready*

# Wrap the binary with the script for debugging inside the container
# mv usr/bin/qt-egl-test usr/bin/qt-egl-test.bin
# cp ../qt-egl-test usr/bin/qt-egl-test

tar -zcf ../qt-egl-test.tar.gz *
