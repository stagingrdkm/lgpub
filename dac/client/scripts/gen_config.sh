#!/bin/sh

PLATFORM=$1

cp config.json.template config.json

echo "Platform: $PLATFORM"

EXTRA_ENV=$(sed '/^[[:space:]]*$/d' ${DAC_ROOT}platform/$PLATFORM/env.txt | sed 's/\([^ ]*\)[[:space:]]*\([^ ]*\)/  "\1", /')
TEMP=$(sed 's/#EXTRA_ENV#/%s/' config.json)
printf "$TEMP" "$EXTRA_ENV" > config.json
echo "generate extra env: $(echo "$EXTRA_ENV" | wc -l)"

EXTRA_LIBS=$(sed '/^[[:space:]]*$/d' ${DAC_ROOT}platform/$PLATFORM/libs.txt | sed 's/\([^ ]*\)[[:space:]]*\([^ ]*\)/  { "destination": "\1", "source": "\2", "type": "bind", "options": [ "rbind", "nosuid", "nodev", "ro" ] }, /')
TEMP=$(sed 's/#EXTRA_LIBS#/%s/' config.json)
printf "$TEMP" "$EXTRA_LIBS" > config.json
echo "generate extra libs: $(echo "$EXTRA_LIBS" | wc -l)"

${DAC_ROOT}scripts/gen_libs.sh ${DAC_ROOT}platform/$PLATFORM/genlibs.txt ${DAC_ROOT}platform/$PLATFORM/libs_deps.txt 2> .tmp.libs
EXTRA_GENLIBS=$(cat .tmp.libs)
rm -f .tmp.libs
TEMP=$(sed 's/#EXTRA_GENLIBS#/%s/' config.json)
printf "$TEMP" "$EXTRA_GENLIBS" > config.json
echo "generate extra gen libs: $(echo "$EXTRA_GENLIBS" | wc -l)"

EXTRA_FILES=$(sed '/^[[:space:]]*$/d' ${DAC_ROOT}platform/$PLATFORM/files.txt | sed 's/\([^ ]*\)[[:space:]]*\([^ ]*\)/  { "destination": "\1", "source": "\2", "type": "bind", "options": [ "rbind", "nosuid", "nodev", "rw" ] }, /')
TEMP=$(sed 's/#EXTRA_FILES#/%s/' config.json)
printf "$TEMP" "$EXTRA_FILES" > config.json
echo "generate extra files: $(echo "$EXTRA_FILES" | wc -l)"

EXTRA_DEVS=$(sed '/^[[:space:]]*$/d' ${DAC_ROOT}platform/$PLATFORM/devs.txt | sed 's/\([^ ]*\)[[:space:]]*\([^ ]*\)/  { "destination": "\1", "source": "\2", "type": "bind", "options": [ "rbind", "rw" ] }, /')
TEMP=$(sed 's/#EXTRA_DEVS#/%s/' config.json)
printf "$TEMP" "$EXTRA_DEVS" > config.json
echo "generate extra devs: $(echo "$EXTRA_DEVS" | wc -l)"

