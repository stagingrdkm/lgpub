#!/bin/sh
umount -v rootfs
cryptsetup -v --debug luksClose vrootfs
veritysetup -v --debug remove vencrootfs
LOOPDEV=$(losetup -a | grep rootfs.sqsh.verity | cut -f1 -d:)
losetup -v -d $LOOPDEV
