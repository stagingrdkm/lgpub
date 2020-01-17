#!/bin/sh

echo "Generate config"
./scripts/gen_config.sh $1

echo "Fix platform permissions"
./platform/$1/fix_platform.sh

echo "Starting container..."
if [ -f /usr/bin/crun ];then
    /usr/bin/crun run --no-pivot test
else
    /usr/bin/runc run --no-pivot test
fi
