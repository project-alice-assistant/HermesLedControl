#!/bin/bash

echo "############### Respeaker Core V2 installation ########################"
echo "############## Please run this script with sudo #######################"

pip3 uninstall -y gpiozero
pip3 uninstall -y RPi.GPIO

apt-get install -y python-mraa

sed -i -e "s/WorkingDirectory=\/home\/pi\//WorkingDirectory=\/home\/"$(logname)"\//" /etc/systemd/system/snipsledcontrol.service

echo "############################## All done! ##############################"
echo "################################ Enjoy! ###############################"