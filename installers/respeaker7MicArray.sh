#!/usr/bin/env bash
echo "############### Respeaker 7 Mic Array installation #########################"
echo "################ Please run this script with sudo ##########################"

USER=$1
FVENV=$2

sudo -u ${USER} bash <<EOF
    source ${FVENV}/bin/activate
    pip3 uninstall -y gpiozero
    pip3 uninstall -y RPi.GPIO

    pip3 --no-cache-dir install respeaker
    pip3 --no-cache-dir install numpy
EOF

echo "############################## All done! ##############################"
echo "############## Don't forget to turn on the SPI interface! #############"