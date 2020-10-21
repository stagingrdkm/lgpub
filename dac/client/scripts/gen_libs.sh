#!/bin/sh

if [ ! -e "$1" ]; then
    exit 0
fi

readelf=$(which eu-readelf || which readelf)

while read p; do
  libname_container=$(echo $p | cut -d' ' -f1)
  libname_container_basename=$(echo $libname_container | sed 's/.*\///')
  libname_host=$(echo $p | cut -d' ' -f2)
  if [ ! -z "$libname_container" ]; then
      echo -e "\nchecking $libname_container: \t"
      if [ ! -s "rootfs/$libname_container" ]; then
          echo "File is NOT delivered in container, so bind mounting from host."
          echo "$libname_container $libname_host" | sed '/^[[:space:]]*$/d' | sed  's/\([^ ]*\)[[:space:]]*\([^ ]*\)/  { "destination": "\1", "source": "\2", "type": "bind", "options": [ "rbind", "nosuid", "nodev", "ro" ] }, /' >&2
      else
          echo "File IS delivered in container, so check if this is OK for our graph libs."
          deps=$(cat $2 | grep $libname_container_basename | cut -d ' ' -f 2)
          if [ -z "$deps" ]; then
              echo "NO DEPS so using the container version of the lib" 
          else
              echo "$deps" > .tmp.deps
              notfound=0
              while read dep; do
                  echo -n "$dep"
                  $readelf -V "rootfs/$libname_container" | sed -n '/Version definition section/,$p' | sed -n '/Version needs section/q;p' | grep "$dep$" > /dev/null 2>&1
                  if [ "$?" = "0" ]; then
                      echo " FOUND"
                  else
                      echo " NOT FOUND so linking in our lib!!!"
                      echo "$libname_container $libname_host" | sed '/^[[:space:]]*$/d' | sed 's/\([^ ]*\)[[:space:]]*\([^ ]*\)/  { "destination": "\1", "source": "\2", "type": "bind", "options": [ "rbind", "nosuid", "nodev", "ro" ] }, /' >&2
                      notfound=1
                      break
                  fi
              done < .tmp.deps 
              if [ $notfound -eq 0 ]; then
                  echo "ALL deps are found so using the container version of the lib"
              fi
              rm -f .tmp.deps
          fi
      fi
  fi
done < $1
