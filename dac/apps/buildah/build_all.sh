#!/bin/bash

buildah unshare ./build.sh wayland-egl-test latest

buildah unshare ./build.sh qt-egl-test latest

buildah unshare ./build.sh gtk-egl-test latest

buildah unshare ./build.sh flutter
 
buildah unshare ./build.sh you.i 

buildah unshare ./build.sh wayland-egl-test-multi
