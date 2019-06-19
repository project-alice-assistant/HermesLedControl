#!/bin/bash
echo "############### Respeaker Core V2 installation ########################"
echo "############## Please run this script with sudo #######################"

pip3.5 uninstall -y gpiozero
pip3.5 uninstall -y RPi.GPIO

apt-get install -y python-mraa

echo "############################## All done! ##############################"
echo "################################ Enjoy! ###############################"