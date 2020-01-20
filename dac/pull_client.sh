#!/bin/sh

if [ -z $1 ]; then
    echo "Usage:"
    echo "pull_client.sh ipaddress_of_box"
    exit 1
fi
scp -r root@$1:/home/root/client/scripts/* client/scripts/
scp -r root@$1:/home/root/client/platform/* client/platform/
