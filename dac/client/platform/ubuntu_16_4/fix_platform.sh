if [ ! -S "/tmp/wayland-1" ]; then
    XDG_RUNTIME_DIR=/tmp weston --socket=wayland-1 &
    sleep 1 
fi

chmod 777 /tmp/wayland-1
