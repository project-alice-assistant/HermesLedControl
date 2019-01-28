#!/usr/bin/env bash

echo "############### Respeaker Core V2 installation ########################"
echo "############## Please run this script with sudo #######################"

if [[ $(logname) != "respeaker" ]]; then
    echo "Cannot install respeaker Core V2 with another user than respeaker"
    exit
fi

pip uninstall -y gpiozero
pip uninstall -y RPi.GPIO
pip --no-cache-dir install pydbus
pip --no-cache-dir install pixel-ring

sed -i -e "s/WorkingDirectory=\/home\/pi\//WorkingDirectory=\/home\/respeaker\//" /etc/systemd/system/snipsledcontrol.service

cd /home/respeaker
rm /home/respeaker/install_all.sh
wget https://raw.githubusercontent.com/respeaker/respeakerd/master/scripts/install_all.sh
sudo su respeaker ./install_all.sh
#cp -f /home/respeaker/respeakerd/scripts/pixel_ring_server /usr/local/bin/
#chmod a+x /usr/local/bin/pixel_ring_server

echo "############################## All done! ##############################"
echo "############## Don't forget to turn on the SPI interface! #############"