#!/bin/sh

echo "Generate config"
./scripts/gen_config.sh $1

echo "Fix platform permissions"
./platform/$1/fix_platform.sh

IS_VERITY_IMAGE=0
if [ -f rootfs.sqsh.verity ]; then
  echo Detected verity image!
  IS_VERITY_IMAGE=1
fi

echo "Starting container..."
if [ -f /usr/bin/crun ] && [ $IS_VERITY_IMAGE == 0 ] ;then
    /usr/bin/crun run --no-pivot test
else
    if [ $IS_VERITY_IMAGE == 0 ]; then
        /usr/bin/runc run --no-pivot test
    else
        ./scripts/verity_mount.sh
        /usr/bin/runc run test
    fi
fi
