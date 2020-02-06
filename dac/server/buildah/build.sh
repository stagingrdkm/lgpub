#!/bin/bash
set -e

container=$1
if [ $# -eq 1 ]; then
    from=scratch
    to=latest
elif [ $# -eq 2 ]; then
    from=scratch
    to=$2
elif [ $# -eq 3 ]; then
    from=$2
    to=$3
fi
user=$(whoami)
curdir=$(pwd)

echo "Container config: ./containers/$container/config"
if [[ ! -f "./containers/$container/config" || "$user" != "root" ]]; then
    echo "Usage: buildah unshare ./build [container name]"
    exit 0
fi

echo "From ${from} to ${to}"

. ./containers/$container/config

echo "Creating new container $container from $from"

if [ "$from" = "scratch" ]; then
newcontainer=$(buildah from scratch)
else
newcontainer=$(buildah from ${container}:${from})
fi

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

echo "Write version file"
echo "Version ${to}" > $scratchmnt/version.txt

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

echo "Commit container ${container}_${to}"
buildah commit $newcontainer ${container}:${to}

echo "Pushing container to repo"
#push to docker
#buildah login docker.io
#buildah push localhost/${container}:${to} docker://docker.io/appcontainerstagingrdk/demo:$container

# push to ibm
#buildah login us.icr.io
buildah push localhost/${container}:${to} docker://us.icr.io/appcontainerstagingrdk/$container:${to}

# push to quay
#buildah login quay.io
#buildah push localhost/${container}:${to} docker://quay.io/appcontainerstagingrdk/$container:${to}

echo "Done."
