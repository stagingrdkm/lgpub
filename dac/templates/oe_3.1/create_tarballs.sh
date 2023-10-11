#!/bin/sh

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 api_version rel_type"
    echo "For example: $0 0.1.1 dbg"
    exit 1
fi

API_VERSION=$1
REL_TYPE=$2

make_tarball () {
  HASH=$(cat "$1".json "$1"_libs.json | sha1sum | cut -d' ' -f1)
  #echo HASH="$HASH"
  TARBALL_NAME="$1_$2-$HASH-$3_dac_configs.tgz"
  #echo TARBALL_NAME="$TARBALL_NAME"
  tar czf "$TARBALL_NAME" "$1".json "$1"_libs.json
}

# all .json files in the current directory excluding *_libs.json
files=$(find . -name "*.json" ! -name "*_libs.json" | sort)

MY_TARBALLS=()
echo "Generating tarballs... "
for file in $files; do
  filename=$(basename "$file" .json)
  #echo "  for $filename..."
  make_tarball "$filename" "$API_VERSION" "$REL_TYPE"
  MY_TARBALLS+=("${TARBALL_NAME}")
done

echo "Summary --------> "

for tarball in "${MY_TARBALLS[@]}"; do
  platform=$(echo "$tarball" | cut -d'_' -f1)
  hash=$(echo "$tarball" | cut -d'_' -f2 | cut -d'-' -f2)

  # Print the formatted output
  echo "# $platform"
  echo "#   yocto 3.1:"
  echo "#     FIRMWARE = \"$API_VERSION-$hash-$REL_TYPE\""
done
