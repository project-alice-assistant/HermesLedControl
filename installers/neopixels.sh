#!/usr/bin/env bash
echo "######################### Neopixels installation ##########################"
echo "#################### Please run this script with sudo #####################"

USER=$(logname)

sed -i -e "\$acore_freq=250" /boot/config.txt
apt-get install swig

pip3 install rpi-ws281x

echo "###################################### All done! #######################################"
echo "##################### Don't forget to turn on the SPI interface! #######################"