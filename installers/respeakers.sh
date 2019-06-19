#!/bin/bash
echo "######################### Respeakers installation #########################"
echo "#################### Please run this script with sudo #####################"

USER=$(logname)

cd /home/${USER}
rm -rf /home/${USER}/seeed-voicecard

git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
chmod +x ./install.sh
./install.sh

echo "###################################### All done! #######################################"
echo "##################### Don't forget to turn on the SPI interface! #######################"