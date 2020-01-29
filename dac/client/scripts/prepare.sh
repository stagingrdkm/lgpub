#!/bin/sh

# flush for simple support on EOS boxes
iptables -F

# check if date is correctly set
curl -s https://www.google.com >/dev/null
if [ $? -eq 60 ]; then
    echo "Is current date $(date)?"
    echo "If not, please run:"
    echo "killall -9 ntpd"
    echo "ntpd -n -d -q -g time.nrc.ca"
    exit 0
fi

