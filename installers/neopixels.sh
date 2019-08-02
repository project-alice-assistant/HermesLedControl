#!/usr/bin/env bash
echo "######################### Neopixels installation ##########################"
echo "#################### Please run this script with sudo #####################"

USER=$1
FVENV=$2

sed -i -e "\$acore_freq=250" /boot/config.txt
apt-get install swig

sudo -u ${USER} bash <<EOF
    source ${FVENV}/bin/activate
    pip3 install rpi-ws281x
EOF

echo "###################################### All done! #######################################"
echo "##################### Don't forget to turn on the SPI interface! #######################"