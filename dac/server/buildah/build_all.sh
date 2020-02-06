#!/bin/bash

buildah unshare ./build.sh wayland-egl-test 1.0
buildah unshare ./build.sh wayland-egl-test 1.0 2.0
buildah unshare ./build.sh wayland-egl-test 2.0 latest


buildah unshare ./build.sh flutter

 
buildah unshare ./build.sh you.i 
