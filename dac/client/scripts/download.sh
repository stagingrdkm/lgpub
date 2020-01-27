#!/bin/sh

# flush for simple support on EOS boxes (do not flush on Xi6)
if [[ $(hostname -s) != *xi6* ]]; then
    iptables -F
fi


# check if date is correctly set
curl -s https://www.google.com >/dev/null
if [ $? -eq 60 ]; then
    echo "Is current date $(date)?"
    echo "If not, please run:"
    echo "killall -9 ntpd"
    echo "ntpd -n -d -q -g time.nrc.ca"
    exit 0
fi


# config data
PACKAGE=appcontainerstagingrdk/demo

# possible tags: wayland-egl-test, flutter, you.i
TAG=flutter
if [ -z $1 ]; then
    TAG=flutter
else
    TAG=$1
fi
echo Downloading TAG: $TAG

SERVER=https://registry-1.docker.io
AUTHSERVER=auth.docker.io
 
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
 
echo "Doing docker auth"
# get auth token]
token=$(curl -s "https://$USERNAME:$PASSWORD@$AUTHSERVER/token?account=$USERNAME&scope=repository:$PACKAGE:pull&service=registry.docker.io" | jq --raw-output '.token')
# echo token=$token
if [ -z $token ]; then
    echo "Unable to authenticate"
    exit 1
fi
 
# download the manifest and store the headers
curl -sL -H "Accept: application/vnd.oci.image.manifest.v1+json" -H "Authorization: Bearer $token"  "$SERVER/v2/$PACKAGE/manifests/$TAG" -o download/manifest.json -D download/manifest.headers
 
# parse manifest and headers to know manifest/config/layer digests
MANIFEST_DIGEST=$(cat download/manifest.headers | grep -i etag | head -n 1 | cut -d: -f3 | cut -d\" -f1)
MANIFEST_SIZE=$(ls -la download/manifest.json  | awk '{print($5)}')
CONFIG_DIGEST=$(cat download/manifest.json | jq '.config.digest' | sed 's/"sha256:\(.*\)"/\1/')
LAYER_DIGESTS=$(cat download/manifest.json | jq '.layers[].digest' | sed 's/"sha256:\(.*\)"/\1/')
 
# output the learned info
echo manifest: $MANIFEST_DIGEST
echo manifest size: $MANIFEST_SIZE
echo config: $CONFIG_DIGEST
echo layer: $LAYER_DIGESTS
 
# create the default index.json and oci-layout file
echo "{\"schemaVersion\":2,\"manifests\":[{\"mediaType\":\"application/vnd.oci.image.manifest.v1+json\",\"digest\":\"sha256:$MANIFEST_DIGEST\",\"size\":$MANIFEST_SIZE}]}" > download/index.json
echo '{"imageLayoutVersion": "1.0.0"}' > download/oci-layout
 
# download and copy all other files
cp download/manifest.json download/blobs/sha256/$MANIFEST_DIGEST
curl -sL -H "Accept: application/vnd.oci.image.manifest.v1+json" -H "Authorization: Bearer $token" "$SERVER/v2/$PACKAGE/blobs/sha256:$CONFIG_DIGEST" -o download/blobs/sha256/$CONFIG_DIGEST
for LAYER in $LAYER_DIGESTS
do
    curl -sL -H "Accept: application/vnd.oci.image.manifest.v1+json" -H "Authorization: Bearer $token" "$SERVER/v2/$PACKAGE/blobs/sha256:$LAYER" -o download/blobs/sha256/$LAYER
done
 
# cleanup old info
rm download/manifest.*
rm -f config.json config.json.template

