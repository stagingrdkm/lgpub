#!/bin/sh

PLATFORM=$1

cp config.json.template config.json

echo "Platform: $PLATFORM"

EXTRA_ENV=$(sed '/^[[:space:]]*$/d s/\([^ ]*\)[[:space:]]*\([^ ]*\)/  "\1", /' platform/$PLATFORM/env.txt)
TEMP=$(sed 's/#EXTRA_ENV#/%s/' config.json)
printf "$TEMP" "$EXTRA_ENV" > config.json
echo "generate extra env: $(echo "$EXTRA_ENV" | wc -l)"

EXTRA_LIBS=$(sed '/^[[:space:]]*$/d s/\([^ ]*\)[[:space:]]*\([^ ]*\)/  { "destination": "\1", "source": "\2", "type": "bind", "options": [ "rbind", "nosuid", "nodev", "ro" ] }, /' platform/$PLATFORM/libs.txt)
TEMP=$(sed 's/#EXTRA_LIBS#/%s/' config.json)
printf "$TEMP" "$EXTRA_LIBS" > config.json
echo "generate extra libs: $(echo "$EXTRA_LIBS" | wc -l)"

EXTRA_FILES=$(sed '/^[[:space:]]*$/d s/\([^ ]*\)[[:space:]]*\([^ ]*\)/  { "destination": "\1", "source": "\2", "type": "bind", "options": [ "rbind", "nosuid", "nodev", "rw" ] }, /' platform/$PLATFORM/files.txt)
TEMP=$(sed 's/#EXTRA_FILES#/%s/' config.json)
printf "$TEMP" "$EXTRA_FILES" > config.json
echo "generate extra files: $(echo "$EXTRA_FILES" | wc -l)"

EXTRA_DEVS=$(sed '/^[[:space:]]*$/d s/\([^ ]*\)[[:space:]]*\([^ ]*\)/  { "destination": "\1", "source": "\2", "type": "bind", "options": [ "rbind", "rw" ] }, /' platform/$PLATFORM/devs.txt)
TEMP=$(sed 's/#EXTRA_DEVS#/%s/' config.json)
printf "$TEMP" "$EXTRA_DEVS" > config.json
echo "generate extra devs: $(echo "$EXTRA_DEVS" | wc -l)"

