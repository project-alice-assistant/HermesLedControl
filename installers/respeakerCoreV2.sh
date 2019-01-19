#!/usr/bin/env bash

echo "############### Respeaker Core V2 installation ########################"
echo "############## Please run this script with sudo #######################"

pip uninstall -y gpiozero
curl https://raw.githubusercontent.com/respeaker/respeakerd/master/scripts/install_all.sh|bash
cp -f ~/respeakerd/scripts/pixel_ring_server /usr/local/bin/
chmod a+x /usr/local/bin/pixel_ring_server
pixel_ring_server

echo "############################## All done! ##############################"
echo "############## Don't forget to turn on the SPI interface! #############"