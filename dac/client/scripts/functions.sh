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
