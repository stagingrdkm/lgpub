#!/bin/bash
set -e

if [ $# -lt 3 ]; then
    echo "Usage: ./flatpak-export.sh [app id] [destination dir] [app] [app path]"
    echo "Usage: ./flatpak-export.sh [app id] [destination dir] [dir] [dir path]"
    exit 0
fi

script_path=$(dirname $(realpath $0))
appid=$1
destination_path=$(realpath $2)
com=$3
com_arg=$4

echo "script path: $script_path"
echo "app id: $appid"
echo "destination path: $destination_path"
echo "command: $com"
echo "command arg: $com_arg"
echo 

if [[ "$com" = "app" || "$com" = "dir" ]]; then
    echo "Check if flatpak app [$appid] is installed?"
    flatpak info $appid > /dev/null
    if [ ! $? -eq 0 ]; then
        echo "NOT INSTALLED!?"
        exit 1
    fi
    echo "OK INSTALLED"

fi
echo "Check destination path $destination_path"
if [ ! -d $destination_path ]; then
    echo "Destination path is NOT a directory?"
    exit 1
fi
echo "OK DIR"


copyPart()
{
    source=$1
    destination=$2
    if [ ! $# -eq 2 ]; then
        return
    fi
    if [ -z $destination ]; then
        return
    fi
    if [ -d ${destination} ]; then
        if [ -d ${source} ]; then
            echo "source is dir"
            source_path=$(dirname $source)
            mkdir -p ${destination}/${source_path}
            cp -R ${source} ${destination}/${source_path}/
        elif [ -e ${source} ]; then
            #echo "source is file"
            source_path=$(dirname $source)
            mkdir -p ${destination}/${source_path}
            cp ${source} ${destination}/${source_path}/ 
        else
            echo "source does not exists?"
        fi
    fi
}

if [ "$com" = "sh" ]; then
    flatpak run --command=sh --devel --filesystem=$script_path --filesystem=$destination_path $appid 




elif [ "$com" = "app" ]; then
    echo "app command"
    flatpak run --devel --filesystem=$script_path --filesystem=$destination_path --command=$script_path/flatpak-export.sh $appid "$appid" "$destination_path" app_internal "$com_arg"

    # dirty hack we use the EGL and GLES from our host
    if [ -e $destination_path/usr/lib/x86_64-linux-gnu/libGLESv2.so.2 ]; then
        cp /usr/lib/x86_64-linux-gnu/libGLESv2.so $destination_path/usr/lib/x86_64-linux-gnu/libGLESv2.so.2
    fi
    if [ -e $destination_path/usr/lib/x86_64-linux-gnu/libEGL.so.1 ]; then
        cp /usr/lib/x86_64-linux-gnu/libEGL.so $destination_path/usr/lib/x86_64-linux-gnu/libEGL.so.1
    fi
elif [ "$com" = "app_internal" ]; then
    echo "app internal command"
    realapp=$(which $com_arg)
    echo "full app path: $realapp"
    copyPart $realapp $destination_path
    libs=$(ldd $realapp | grep "=>" | sort -u | awk '{print($3)}')
    for lib in $libs
    do
        copyPart $lib $destination_path
    done

    # extra copy EGL libs
    #libs=$(ldd /usr/lib/x86_64-linux-gnu/GL/default/lib/libEGL_mesa.so.0 | grep "=>" | sort -u | awk '{print($3)}')
    #for lib in $libs
    #do
    #    copyPart $lib $destination_path
    #done
    #cp /usr/lib/x86_64-linux-gnu/GL/default/lib/libEGL_mesa.so.0 $destination_path/usr/lib/x86_64-linux-gnu/libEGL.so.1
    #rm $destination_path/usr/lib/x86_64-linux-gnu/libEGL.so.1
    #rm $destination_path/usr/lib/x86_64-linux-gnu/libGLESv2.so.2
    cd $destination_path && find .




elif [ "$com" = "dir" ]; then
    echo "dir command"
    flatpak run --devel --filesystem=$script_path --filesystem=$destination_path --command=$script_path/flatpak-export.sh $appid "$appid" "$destination_path" dir_internal "$com_arg"
elif [ "$com" = "dir_internal" ]; then
    echo "dir internal command"
    copyPart $com_arg $destination_path
    cd $destination_path && find ./$com_arg



else
   echo "UNKNOWN COMMAND: $com"
   exit 1
fi

exit 0
