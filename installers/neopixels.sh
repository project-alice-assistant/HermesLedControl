#!/usr/bin/env bash
echo "######################### Neopixels installation ##########################"
echo "#################### Please run this script with sudo #####################"

sed -i -e "\$acore_freq=250" /boot/config.txt
apt-get install scons

cd /home/pi
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
python setup.py install

echo "###################################### All done! #######################################"
echo "##################### Don't forget to turn on the SPI interface! #######################"