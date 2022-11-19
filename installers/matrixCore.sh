#!/usr/bin/env bash
echo "######################## Matrix Core installation ########################"
echo "######################### Please run this script with sudo ##########################"

USER=$1
FVENV=$2

sudo -u ${USER} bash <<EOF
    source ${FVENV}/bin/activate
    pip3 uninstall -y gpiozero
    pip3 uninstall -y RPi.GPIO
    pip3 --no-cache-dir install matrix-io-proto==0.0.32
    pip3 --no-cache-dir install protobuf==3.20.1
    pip3 --no-cache-dir install pyzmq==24.0.1
EOF

echo "######################## All done! ########################"
echo "################## Enjoy SLC! Psycho ######################"
