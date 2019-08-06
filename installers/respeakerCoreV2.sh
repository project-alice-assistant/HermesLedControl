#!/usr/bin/env bash
echo "############### Respeaker Core V2 installation ########################"
echo "############## Please run this script with sudo #######################"

USER=$1
FVENV=$2

sudo -u ${USER} bash <<EOF
    source ${FVENV}/bin/activate
    pip3 uninstall -y gpiozero
    pip3 uninstall -y RPi.GPIO
    pip3 --no-cache-dir install numpy
EOF

apt-get install -y python-mraa

echo "############################## All done! ##############################"
echo "################################ Enjoy! ###############################"