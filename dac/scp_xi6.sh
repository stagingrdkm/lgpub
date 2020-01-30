#!/bin/sh

if [ -z $1 ]; then
    echo "Usage:"
    echo "scp_client.sh ipaddress_of_xi6"
    exit 1
fi

EXTRA_SCP_ARGS="-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"

scp $EXTRA_SCP_ARGS -r ./client root@$1:/tmp/
# Xi6 already has runc & crun installed, so just need jq.
scp $EXTRA_SCP_ARGS ./bin/armv7hl/bin/jq root@$1:/tmp/client/jq