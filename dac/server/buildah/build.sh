#!/bin/bash
set -e

container=$1
user=$(whoami)
curdir=$(pwd)

echo "Container config: ./containers/$container/config"
if [[ ! -f "./containers/$container/config" || "$user" != "root" ]]; then
    echo "Usage: buildah unshare ./build [container name]"
    exit 0
fi

. ./containers/$container/config

echo "Creating new container $container"

newcontainer=$(buildah from scratch)
echo "Temp container: $newcontainer"

scratchmnt=$(buildah mount $newcontainer)
echo "Temp mount $scratchmnt"

echo "Unpacking files to temp mount"
for file in $files
do
    filename=$(echo "$file##" | cut -f1 -d#)
    striplevel=$(echo "$file##" | cut -f2 -d#)

    if [ "$striplevel" = "" ]; then
        striplevel=0
    fi

    echo "filename: $filename"
    echo "striplevel: $striplevel"
    if [ -e "$curdir/containers/$container/$filename" ]; then
        echo Unpacking $curdir/containers/$container/$filename
        (cd $scratchmnt && tar xzf $curdir/containers/$container/$filename --strip-components=$striplevel )
    else
        echo "SKIPPING $filename because it does not exist!"
    fi
done

echo "Unmounting container"
buildah umount $newcontainer

echo "Configure container"
buildah config --entrypoint "$cmd" $newcontainer
buildah config --user 0:0 $newcontainer
for single_env in $env
do
    buildah config --env $single_env $newcontainer
done
buildah config --workingdir ${cwd} $newcontainer

echo "Commit container $container"
buildah commit $newcontainer $container

echo "Pushing container to docker"
#buildah login docker.io
buildah push localhost/$container docker://docker.io/appcontainerstagingrdk/demo:$container

echo "Done."
