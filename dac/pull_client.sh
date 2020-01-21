#!/bin/sh

if [ -z $1 ]; then
    echo "Usage:"
    echo "pull_client.sh ipaddress_of_box"
    exit 1
fi

EXTRA_SCP_ARGS="-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
scp $EXTRA_SCP_ARGS -r root@$1:/home/root/client/scripts/* client/scripts/
scp $EXTRA_SCP_ARGS -r root@$1:/home/root/client/platform/* client/platform/
