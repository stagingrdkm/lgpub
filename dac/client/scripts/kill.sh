#!/bin/sh

user=$(whoami)
sudo=""
if [ "$user" != "root" ]; then
    sudo="sudo "
fi

if [ -f /etc/WPEFramework/plugins/OCIContainer.json ]; then
  curl -v --header "Content-Type:application/json" --request POST http://127.0.0.1:9998/jsonrpc --data-raw '{"jsonrpc":"2.0","id":1,"method":"org.rdk.OCIContainer.1.stopContainer", "params":{"containerId":"test"}}'
elif [ -f /usr/bin/DobbyTool ]; then
  DobbyTool -vvv stop test
elif [ -f /usr/bin/crun ]; then
  $sudo killall -9 wayland-egl-test wayland-egl-test-input qt-egl-test gtk-egl-test runc crun flutter-launcher-wayland Auryn flutter-wayland-app
  sleep 2
  crun kill -a test
  crun delete test
else
  $sudo killall -9 wayland-egl-test wayland-egl-test-input qt-egl-test gtk-egl-test runc crun flutter-launcher-wayland Auryn flutter-wayland-app
  sleep 2
  runc kill -a test
  runc delete test
fi

if [ -f rootfs.sqsh.verity ]; then
  echo Detected verity image!
  ${DAC_ROOT}scripts/verity_umount.sh
fi
