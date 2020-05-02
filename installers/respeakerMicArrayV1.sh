#!/usr/bin/env bash
echo "############### Respeaker Mic Array V1 installation ########################"
echo "################ Please run this script with sudo ##########################"

USER=$1
FVENV=$2

sudo -u ${USER} bash <<EOF
    source ${FVENV}/bin/activate
    pip3 install click
    pip3 install pyusb
    pip3 --no-cache-dir install numpy
EOF

sed -i -e "s/User="${USER}"/User=root/" /etc/systemd/system/hermesledcontrol.service

echo "############################## All done! ##############################"
echo "############## Don't forget to turn on the SPI interface! #############"
