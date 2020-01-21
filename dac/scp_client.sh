#!/bin/sh

if [ -z $1 ]; then
    echo "Usage:"
    echo "scp_client.sh ipaddress_of_box"
    echo "  !!  might need 'mount -o remount,rw /' on box first"
    exit 1
fi

EXTRA_SCP_ARGS="-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
scp $EXTRA_SCP_ARGS ./bin/armv7hl/bin/* root@$1:/usr/bin
scp $EXTRA_SCP_ARGS ./bin/armv7hl/lib/* root@$1:/usr/lib
scp $EXTRA_SCP_ARGS -r ./client root@$1:/home/root
