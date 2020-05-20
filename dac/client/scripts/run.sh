#!/bin/sh

. ${DAC_ROOT}scripts/functions.sh

echo "Generate config"
${DAC_ROOT}scripts/gen_config.sh $1

echo "Fix platform permissions"
${DAC_ROOT}platform/$1/fix_platform.sh

RUN_ARGS=""
if [ -f rootfs.sqsh.verity ]; then
    echo Detected verity image!
    ${DAC_ROOT}scripts/verity_mount.sh
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
