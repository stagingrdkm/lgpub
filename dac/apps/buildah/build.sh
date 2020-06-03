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

echo "Container config: ./containers/$container/config*"
if [[ ! -f "./containers/$container/archs" || "$user" != "root" ]]; then
    echo "Usage: buildah unshare ./build [container name]"
    exit 0
fi

echo "From ${from} to ${to}"


archs=$(cat ./containers/$container/archs)
no_archs=$(wc -l ./containers/$container/archs | cut -d' ' -f1)
echo "Number of architectures: $no_archs"

for arch in $archs
do
    . ./containers/$container/config_${arch}

    echo 
    echo 
    echo "Creating new container $container from $from (arch: $arch)"

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
    #add arch+os https://golang.org/doc/install/source#environment
    buildah config --arch ${arch} $newcontainer
    buildah config --os linux $newcontainer


    if [ $no_archs -eq 1 ]; then
        echo "Commit container ${container}_${to}"
        buildah commit $newcontainer ${container}:${to}

        echo "Pushing single arch container to repo"
        # push to ibm
        #buildah login us.icr.io
        buildah push localhost/${container}:${to} docker://us.icr.io/appcontainerstagingrdk/${container}:${to}
    else
        echo "Commit container ${container}_${to}"
        buildah commit $newcontainer ${container}_${arch}:${to}
    fi
done

if [ ! $no_archs -eq 1 ]; then
    echo
    echo
    echo "Removing possible old version of container ${container}"
    buildah rmi -f ${container} || true
    echo "Creating manifest container ${container}"
    buildah manifest create ${container} 

    echo "Adding arch containers into the manifest"
    for arch in $archs
    do
        echo "Adding ${arch}"
        buildah manifest add ${container} localhost/${container}_${arch}:${to}
    done

    echo "Inspect local copy of the manifest container"
    buildah manifest inspect ${container} 

    echo "Pushing the manifest multi arch container to the registry"
    buildah manifest push --all ${container} docker://us.icr.io/appcontainerstagingrdk/$container:${to}
fi

echo "Done."
