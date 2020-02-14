#!/bin/sh

. ./scripts/functions.sh

if [[ ! -d ./platform/$1 || ! $# -eq 1 ]]; then
    echo "Usage: ./scripts/run.sh [platformname]"
    exit 0
fi

echo "Generate config"
./scripts/gen_config.sh $1

echo "Fix platform permissions"
./platform/$1/fix_platform.sh

RUN_ARGS=""
if [ -f rootfs.sqsh.verity ]; then
    echo Detected verity image!
    ./scripts/verity_mount.sh
else
    # --no-pivot needed for rootfs on ramfs
    RUN_ARGS="--no-pivot"
fi

user=$(whoami)
sudo=""
if [ "$user" != "root" ]; then
    sudo="sudo "
    prepareBindMountsAndRootfs
fi

echo "Starting container..."
if [ -f /usr/bin/crun ]; then
    $sudo crun run $RUN_ARGS test
elif [ -f /usr/local/bin/crun ]; then
    $sudo crun run $RUN_ARGS test
else
    $sudo runc run $RUN_ARGS test
fi
