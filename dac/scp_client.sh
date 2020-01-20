#!/bin/sh

if [ -z $1 ]; then
    echo "Usage:"
    echo "scp_client.sh ipaddress_of_box"
    echo "  !!  might need 'mount -o remount,rw /' on box first"
    exit 1
fi
scp ./bin/armv7hl/bin/* root@$1:/usr/bin
scp ./bin/armv7hl/lib/* root@$1:/usr/lib
scp -r ./client root@$1:/home/root
