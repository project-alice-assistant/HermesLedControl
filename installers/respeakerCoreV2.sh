#!/usr/bin/env bash
echo "############### Respeaker Core V2 installation ########################"
echo "############## Please run this script with sudo #######################"

pip3 uninstall -y gpiozero
pip3 uninstall -y RPi.GPIO
pip3 install python3-numpy

apt-get install -y python-mraa

echo "############################## All done! ##############################"
echo "################################ Enjoy! ###############################"