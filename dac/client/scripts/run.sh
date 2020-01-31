#!/bin/sh

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

echo "Starting container..."
if [ -f /usr/bin/crun ]; then
    /usr/bin/crun run $RUN_ARGS test
else
    /usr/bin/runc run $RUN_ARGS test
fi
