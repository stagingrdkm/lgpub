# Example DAC applications

## wayland-egl-test

**Description:** Source code example of simple Wayland EGL application intended as tutorial for developers. Contains the few but necessary setup code for any direct to wayland-egl client application such as how to connect to wayland server, create/use EGL surface and draw on screen via opengles api. Application shows simple rectangle on screen. Applications based on this example should run on the various wayland compositors supporting the wayland-egl protocol out there.  
**Source:** https://github.com/dwrobel/tutorials/blob/glesv2/wayland-egl.c  
**Yocto recipe:** https://github.com/dwrobel/tutorials/blob/glesv2/wayland-egl-test.bb

Example pull for the single package:  
docker pull us.icr.io/appcontainerstagingrdk/wayland-egl-test  
buildah pull docker://us.icr.io/appcontainerstagingrdk/wayland-egl-test  

Example pull for the multi architecture package:  
docker pull us.icr.io/appcontainerstagingrdk/wayland-egl-test-multi  
buildah pull docker://us.icr.io/appcontainerstagingrdk/wayland-egl-test-multi  

## you.i

**Description:**  Showcase application from the company https://www.youi.tv/. The container package contains both the react native application and the You.i TV react native Gfx engine beneath.  
Compiled with firebolt sdk  
**Source:**  Closed source, binary only

Example pull for the single package:  
docker pull us.icr.io/appcontainerstagingrdk/you.i  
buildah pull docker://us.icr.io/appcontainerstagingrdk/you.i  

## flutter

**Description:**  Container contains both Flutter application and Flutter engine running on wayland-egl, developed by Liberty Global while evaluating Google Flutter UI toolkit https://flutter.dev/  
Flutter Application is compiled on Linux PC in ahead of time (AOT) compilation mode.  
**Source:**  Application is closed source. Flutter engine is open source on https://github.com/flutter/engine 

Example pull for the single package:  
docker pull us.icr.io/appcontainerstagingrdk/flutter  
buildah pull docker://us.icr.io/appcontainerstagingrdk/flutter  

Example pull for the multi architecture package:  
docker pull us.icr.io/appcontainerstagingrdk/flutter-multi  
buildah pull docker://us.icr.io/appcontainerstagingrdk/flutter-multi  
