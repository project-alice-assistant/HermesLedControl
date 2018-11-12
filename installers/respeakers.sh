#!/usr/bin/env bash

echo "######################### Respeakers installation #########################"
echo "#################### Please run this script with sudo #####################"

if [[ -d "/var/lib/snips/skills/snips-skill-respeaker" ]]; then
    rm -rf "/var/lib/snips/skills/snips-skill-respeaker"
    systemctl restart snips-*
    echo "Removed snips-skill-respeaker"
fi

cd /home/pi
rm -rf /home/pi/seeed-voicecard
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
chmod +x ./install.sh
./install.sh

echo "###################################### All done! #######################################"
echo "##################### Don't forget to turn on the SPI interface! #######################"