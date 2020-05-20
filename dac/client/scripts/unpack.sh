#!/bin/sh

. ${DAC_ROOT}scripts/functions.sh

# cleanup old rootfs

rm -rf rootfs 
mkdir -p rootfs 
rm -f rootfs.sqsh.verity* verity.conf

# get the correct MANIFES_DIGEST
arch=$(getOCIArch)
echo arch=$arch
MANIFEST_DIGEST=$(cat download/index.json  | jq ".manifests[] | select(.platform.architecture==\"$arch\") | .digest" | sed 's/^"//' | sed 's/"$//' | cut -d: -f 2)
echo "manifest for ${arch} is ${MANIFEST_DIGEST}"

# parse the config and layer digests
LAYER_DIGESTS=$(cat download/blobs/sha256/$MANIFEST_DIGEST | jq '.layers[].digest' | sed 's/"sha256:\(.*\)"/\1/')
CONFIG_DIGEST=$(cat download/blobs/sha256/$MANIFEST_DIGEST | jq '.config.digest' | sed 's/"sha256:\(.*\)"/\1/')

echo manifest: $MANIFEST_DIGEST
echo layers: $LAYER_DIGESTS
echo config: $CONFIG_DIGEST

# extra the layer tarballs and delete the .wh. files
for LAYER in $LAYER_DIGESTS
do
    echo layer: $LAYER
    tar -tzf download/blobs/sha256/$LAYER > /dev/null 2>&1
    if [ $? == 0 ]; then
        DELETE_LIST=$(tar tzf download/blobs/sha256/$LAYER)
        echo $DELETE_LIST | grep '\.wh\.\.wh\.\.opq' | sed 's/\.wh\.\.wh\.\.opq//' | awk '{print("rm -rf rootfs/"$1"*")}'
        echo $DELETE_LIST | grep '\.wh\.\.wh\.\.opq' | sed 's/\.wh\.\.wh\.\.opq//' | awk '{system("rm -rf rootfs/"$1"*")}'
        echo $DELETE_LIST | grep "\.wh\."            | sed 's/\.wh\.//'            | awk '{print("rm -rf rootfs/"$1)}'
        echo $DELETE_LIST | grep "\.wh\."            | sed 's/\.wh\.//'            | awk '{system("rm -rf rootfs/"$1)}'
        tar xzf download/blobs/sha256/$LAYER -C rootfs | grep -v '\.wh\.'
        find rootfs/ -name "\.wh\.*" -type f -exec rm {} \;
    else
        echo Detected verity image!
        # not a tarball but gzipped encrypted verity image
        cp download/blobs/sha256/$LAYER rootfs.sqsh.verity.gz
        gunzip rootfs.sqsh.verity.gz
        # create verity.conf from Labels annotations
        root_hash=$(jq '.config.Labels["com.libertyglobal.dac.root_hash"]' download/blobs/sha256/$CONFIG_DIGEST)
        hash_offset=$(jq '.config.Labels["com.libertyglobal.dac.hash_offset"]' download/blobs/sha256/$CONFIG_DIGEST)
        echo root_hash=$root_hash > verity.conf
        echo hash_offset=$hash_offset >> verity.conf
    fi
done

# helper function
generateList()
{
    FULL=""
    for PART in $2
    do
        if [ "$FULL" != "" ]; then 
            FULL="$FULL," 
        fi
        FULL="$FULL $PART"
    done
    echo "$FULL"
}

# generate the config.json.template
# using cmd, entrypoint, env, volumes, workingdir, user information from OCI config file
cp ${DAC_ROOT}scripts/config.json.template config.json.template

ARCH=$(cat download/blobs/sha256/$CONFIG_DIGEST | jq '.architecture' 2> /dev/null)
OS=$(cat download/blobs/sha256/$CONFIG_DIGEST | jq '.os' 2> /dev/null)
echo "Architecture: $ARCH"
echo "OS: $OS"

CONFIG_ENTRYPOINT=$(cat download/blobs/sha256/$CONFIG_DIGEST | jq '.config.Entrypoint[]' 2> /dev/null)
CONFIG_CMD=$(cat download/blobs/sha256/$CONFIG_DIGEST | jq '.config.Cmd[]' 2> /dev/null)
if [ ! -z "$CONFIG_ENTRYPOINT" ]; then
    CONFIG_CMD="$CONFIG_ENTRYPOINT $CONFIG_CMD"
fi
if [ ! -z "$CONFIG_CMD" ]; then
    FULL_CMD=$(generateList CONFIG_CMD "$CONFIG_CMD")
else
    FULL_CMD=""
fi
echo "FULL_CMD $FULL_CMD"
TEMP=$(sed 's/#CONFIG_ARGS#/%s/' config.json.template)
printf "$TEMP" "$FULL_CMD" > config.json.template


CONFIG_ENV=$(cat download/blobs/sha256/$CONFIG_DIGEST | jq '.config.Env[]' 2> /dev/null)
if [ ! -z "$CONFIG_ENV" ]; then
    FULL_ENV=$(generateList CONFIG_ENV "$CONFIG_ENV")
    FULL_ENV="$FULL_ENV,"
else
    FULL_ENV=""
fi
echo "CONFIG_ENV $FULL_ENV"
TEMP=$(sed 's/#CONFIG_ENV#/%s/' config.json.template)
printf "$TEMP" "$FULL_ENV" > config.json.template

CONFIG_VOLUMES=$(cat download/blobs/sha256/$CONFIG_DIGEST | jq '.config.Volumes[]' 2> /dev/null)
if [ ! -z "$CONFIG_VOLUMES" ]; then
    CONFIG_MOUNTS=$(echo $CONFIG_VOLUMES | sed '/^\([^ ]*\)/  { "destination": "\1", "source": "\1", "type": "bind", "options": [ "rbind", "nosuid", "nodev", "rw" ] }, /')
    CONFIG_MOUNTS="$CONFIG_MOUNTS,"
else
    CONFIG_MOUNTS=""
fi
echo "CONFIG_MOUNTS $CONFIG_MOUNTS"
TEMP=$(sed 's/#CONFIG_MOUNTS#/%s/' config.json.template)
printf "$TEMP" "$CONFIG_MOUNTS" > config.json.template

CONFIG_CWD=$(cat download/blobs/sha256/$CONFIG_DIGEST | jq '.config.WorkingDir' 2> /dev/null)
if [ -z "$CONFIG_CWD" ]; then
    CONFIG_CWD="/"
fi
echo "CONFIG_CWD $CONFIG_CWD"
TEMP=$(sed 's/#CONFIG_CWD#/%s/' config.json.template)
printf "$TEMP" "$CONFIG_CWD" > config.json.template

CONFIG_USERGROUP=$(cat download/blobs/sha256/$CONFIG_DIGEST | jq '.config.User' | sed 's/\"//g' 2> /dev/null)
if [ -z "CONFIG_USERGROUP" ]; then
    CONFIG_USERGROUP="0:0"
fi
USER=$(echo $CONFIG_USERGROUP | cut -d ':' -f 1)
GROUP=$(echo $CONFIG_USERGROUP | cut -d ':' -f 2)
echo "CONFIG_USER $USER"
echo "CONFIG_GROUP $GROUP"
TEMP=$(sed 's/#CONFIG_USER#/%s/' config.json.template)
printf "$TEMP" "\"uid\": $USER, \"gid\": $GROUP" > config.json.template
