#!/bin/sh

# helper function to get CPU Architecture in OCI format
getOCIArch()
{
    arch=$(uname -m)
    if [ "$arch" = "x86_64" ]; then
        arch="amd64"
    elif [ "$arch" = "armv7l" ]; then
        arch="arm"
    fi
    
    echo $arch
}

# helper function to prepare the bind mounts as files and dir
prepareBindMountsAndRootfs()
{
    echo "Preparing bind mounts"
    cat config.json | jq -r '.mounts[] | [.source, .destination] | join(" ")' > .tmp.mounts
    while read bmount; do
        source=$(echo "$bmount" | cut -d' ' -f1)
        destination=$(echo "$bmount" | cut -d' ' -f2)
        echo "$source -> $destination"
        if [ -d $source ]; then
            mkdir -p rootfs$destination
        elif [ -e $source ]; then
            mkdir -p rootfs$(dirname $destination)
            touch rootfs$destination
            chmod 777 rootfs$(dirname $destination)
            chmod 777 rootfs$destination
        else
            mkdir -p rootfs$destination
        fi
    done < .tmp.mounts
    rm -f .tmp.mounts

    # fix file permissions for crun/runc
    chmod -R o+rx rootfs
}
