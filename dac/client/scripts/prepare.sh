#!/bin/sh

# flush for simple support on EOS boxes (do not flush on Xi6)
if [[ $(hostname -s) != *xi6* ]]; then
    iptables -F
fi

# check if date is correctly set
curl -s https://www.google.com >/dev/null
if [ $? -eq 60 ]; then
    echo "Is current date $(date)?"
    echo "If not, please run:"
    echo "killall -9 ntpd"
    echo "ntpd -n -d -q -g time.nrc.ca"
    exit 1
fi
