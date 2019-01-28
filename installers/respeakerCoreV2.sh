#!/usr/bin/env bash

echo "############### Respeaker Core V2 installation ########################"
echo "############## Please run this script with sudo #######################"

if [[ $(logname) != "respeaker" ]]; then
    echo "Cannot install respeaker Core V2 with another user than respeaker"
    exit
fi

pip uninstall -y gpiozero
pip uninstall -y RPi.GPIO

#cd /home/respeaker
#rm -rf /home/respeaker/respeakerd
#wget https://raw.githubusercontent.com/respeaker/respeakerd/master/scripts/install_all.sh
#su respeaker ./install_all.sh


systemctl is-active -q pixel_ring_server && systemctl stop pixel_ring_server
pip uninstall -y pixel_ring

sed -i -e "s/WorkingDirectory=\/home\/pi\//WorkingDirectory=\/home\/respeaker\//" /etc/systemd/system/snipsledcontrol.service

echo "############################## All done! ##############################"
echo "############## Don't forget to turn on the SPI interface! #############"