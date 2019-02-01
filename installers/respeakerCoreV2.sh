#!/usr/bin/env bash

echo "############### Respeaker Core V2 installation ########################"
echo "############## Please run this script with sudo #######################"

systemctl is-active -q pixel_ring_server && systemctl stop pixel_ring_server
pip uninstall -y pixel_ring
pip uninstall -y gpiozero
pip uninstall -y RPi.GPIO

apt-get install -y python-mraa
apt-get install -y python-upm
apt-get install -y libmraa1
apt-get install -y libupm1
apt-get install -y mraa-tools

sed -i -e "s/WorkingDirectory=\/home\/pi\//WorkingDirectory=\/home\/"$(logname)"\//" /etc/systemd/system/snipsledcontrol.service

echo "############################## All done! ##############################"
echo "################################ Enjoy! ###############################"