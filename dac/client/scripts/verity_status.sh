#!/bin/sh -x
mount | grep mapper
ls -lsa /dev/mapper
veritysetup status vrootfs
cryptsetup status vencrootfs
