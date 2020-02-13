#!/bin/sh

if [ ! -e "$1" ]; then
    echo "Usage: ./scripts/gen_deps.sh [filename with lib on each line]"
    exit 0
fi

rm -f .tmp.libs

while read p; do
  libname=$(echo $p | cut -d' ' -f2)
  if [ ! -z "$libname" ]; then
      #echo "$libname"
      ldd -v $libname 2> /dev/null | sed -n '/Version information/,$p' >> .tmp.libs
  fi
done < $1

grep "=>" .tmp.libs | sort -u | tr '(' ' ' | tr ')' ' ' | awk '{print($1" "$2)}'

rm -f .tmp.libs
