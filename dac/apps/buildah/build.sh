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

        echo "Processing file: ${filename} striplevel: ${striplevel}"
        file_full_path="$curdir/containers/$container/$filename"
        if [ -e "${file_full_path}" ]; then
            mime_type=$(file --mime-type "${file_full_path}" | cut -d ' ' -f2-)

            echo "Unpacking: ${file_full_path} mime-type: ${mime_type}"

            case "${mime_type}" in
            "application/vnd.debian.binary-package")
                tmpdir=$(mktemp -d);
                (cd "${tmpdir}"; ar -x "${file_full_path}" data.tar.gz) && tar zxf "${tmpdir}/data.tar.gz" -C "${scratchmnt}"
                rm -rf "${tmpdir}"
            ;;
            "application/x-rpm")
                rpm2cpio "${file_full_path}" | cpio -idmv -D "${scratchmnt}"
            ;;
            "application/x-tar")
                tar --no-same-owner  -xf "${file_full_path}" --strip-components=$striplevel -C "${scratchmnt}"
            ;;
            "application/gzip")
                tar --no-same-owner -zxf "${file_full_path}" --strip-components=$striplevel -C "${scratchmnt}"
            ;;
            "application/x-bzip2")
                tar --no-same-owner -jxf "${file_full_path}" --strip-components=$striplevel -C "${scratchmnt}"
            ;;
            "application/x-xz")
                tar --no-same-owner -Jxf "${file_full_path}" --strip-components=$striplevel -C "${scratchmnt}"
            ;;
            *)
                echo "Unsupported mime-type: ${mime_type}"
                exit 2
            ;;
            esac
        else
            echo "Could not find file: ${file_full_path}"
            exit 1
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

    if ! buildah login --get-login us.icr.io 2>/dev/null; then
        buildah login us.icr.io
    fi

    if [ $no_archs -eq 1 ]; then
        echo "Commit container ${container}_${to}"
        buildah commit $newcontainer ${container}:${to}

        echo "Pushing single arch container to repo"
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
