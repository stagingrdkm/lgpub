#!/bin/bash

if [ -z $1 ]; then
    echo "Usage:"
    echo "scp_client.sh <ipaddress_of_box> [directory-with-rw-permission]"
    echo "directory-with-rw-permission - if not specified /home/root will be assumed"
    exit 1
fi

if [ -z $2 ]; then
    DESTDIR="/home/root"
else
    DESTDIR="$2"
fi

echo "Destination directory: ${DESTDIR}"

SCRIPT_DIR=$(cd `dirname $0` && pwd)

EXTRA_SCP_ARGS="-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
scp $EXTRA_SCP_ARGS -r ${SCRIPT_DIR}/client root@$1:${DESTDIR}
