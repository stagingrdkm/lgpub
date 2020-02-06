#!/bin/sh

# possible tags: wayland-egl-test, flutter, you.i
PACKAGE=flutter
if [ -z $1 ]; then
    PACKAGE=flutter
else
    PACKAGE=$1
fi
echo "Downloading: $PACKAGE"
if [ -z "$CONFIG" ]; then
    CONFIG=docker
fi
echo Downloading from: $CONFIG

if [ ! -e ./scripts/$CONFIG.conf ]; then
    echo "Unknown config: ./scripts/$CONFIG.conf"
    exit 0
fi

. ./scripts/$CONFIG.conf

if [ $# -eq 2 ]; then
    TAG=$2
fi
echo "Downloading tag: $TAG"

if [ -z $PASSWORD ]; then
    echo "Please set PASSWORD env var"
    exit 1
fi
if [ -z $USERNAME ]; then
    echo "Please set USERNAME env var"
    exit 1
fi
 
#end config data
 
# cleanup old download and prepare download dir
rm -rf download
mkdir -p download/blobs/sha256

echo "Doing auth"
# get auth token
token="null"
token=$(curl -sL "https://$USERNAME:$PASSWORD@$AUTHSERVER?account=$USERNAME&scope=repository:$NAMESPACE/$REPO:pull&service=$REGISTRY" | jq --raw-output '.token' 2> /dev/null)
#echo token=$token
if [ "$token" = "null" ]; then
    echo "Unable to authenticate"
    exit 1
fi
 
# download the manifest and store the headers
curl -sL -H "Accept: application/vnd.oci.image.manifest.v1+json" -H "Authorization: Bearer $token" "https://$SERVER/v2/$NAMESPACE/$REPO/manifests/$TAG" -o download/manifest.json -D download/manifest.headers
 
# parse manifest and headers to know manifest/config/layer digests
if [ "$CONFIG" = "quay" ]; then

    # quay is returning manifest and headers in docker format
    MANIFEST_DIGEST=$(cat download/manifest.headers | grep -i Docker-Content-Digest | head -n 1 | cut -d: -f3 | cut -d\" -f1 | tr '\n' ' ' | tr '\r' ' ' | sed 's/  //')
    MANIFEST_SIZE=$(ls -la download/manifest.json  | awk '{print($5)}')
    OCICONFIG=$(cat download/manifest.json | jq '.history[0].v1Compatibility' | sed 's/\\//g' | sed 's/^"//' | sed 's/"$//')
    CONFIG_DIGEST=$(echo $OCICONFIG | sha256sum | awk '{print($1)}')
    LAYER_DIGESTS=$(cat download/manifest.json | jq '.fsLayers[0].blobSum' | sed 's/"sha256:\(.*\)"/\1/')

    echo $OCICONFIG > download/blobs/sha256/$CONFIG_DIGEST
    echo "{\"schemaVersion\":2,\"config\":{\"mediaType\":\"application/vnd.oci.image.config.v1+json\",\"digest\":\"sha256:$CONFIG_DIGEST\"},\"layers\":[{\"mediaType\":\"application/vnd.oci.image.layer.v1.tar\",\"digest\":\"sha256:$LAYER_DIGESTS\"}]}" > download/blobs/sha256/$MANIFEST_DIGEST

else

    MANIFEST_DIGEST=$(cat download/manifest.headers | grep -i etag | head -n 1 | cut -d: -f3 | cut -d\" -f1)
    MANIFEST_SIZE=$(ls -la download/manifest.json  | awk '{print($5)}')
    CONFIG_DIGEST=$(cat download/manifest.json | jq '.config.digest' | sed 's/"sha256:\(.*\)"/\1/')
    LAYER_DIGESTS=$(cat download/manifest.json | jq '.layers[].digest' | sed 's/"sha256:\(.*\)"/\1/')

fi

# output the learned info
echo manifest: $MANIFEST_DIGEST
echo manifest size: $MANIFEST_SIZE
echo config: $CONFIG_DIGEST
echo layer: $LAYER_DIGESTS

# create the default index.json and oci-layout file
echo "{\"schemaVersion\":2,\"manifests\":[{\"mediaType\":\"application/vnd.oci.image.manifest.v1+json\",\"digest\":\"sha256:$MANIFEST_DIGEST\",\"size\":$MANIFEST_SIZE}]}" > download/index.json
echo '{"imageLayoutVersion": "1.0.0"}' > download/oci-layout
 
# download and copy all other files
if [ "$CONFIG" != "quay" ]; then
    cp download/manifest.json download/blobs/sha256/$MANIFEST_DIGEST
    curl -sL -H "Accept: application/vnd.oci.image.manifest.v1+json" -H "Authorization: Bearer $token" "https://$SERVER/v2/$NAMESPACE/$REPO/blobs/sha256:$CONFIG_DIGEST" -o download/blobs/sha256/$CONFIG_DIGEST
fi

for LAYER in $LAYER_DIGESTS
do
    curl -sL -H "Accept: application/vnd.oci.image.manifest.v1+json" -H "Authorization: Bearer $token" "https://$SERVER/v2/$NAMESPACE/$REPO/blobs/sha256:$LAYER" -o download/blobs/sha256/$LAYER
done
 
# cleanup old info
rm download/manifest.*
rm -f config.json config.json.template

