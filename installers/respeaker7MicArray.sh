#!/usr/bin/env bash
echo "############### Respeaker 7 Mic Array installation #########################"
echo "################ Please run this script with sudo ##########################"

pip3.5 uninstall -y gpiozero
pip3.5 uninstall -y RPi.GPIO

pip3.5 --no-cache-dir install respeaker

echo "############################## All done! ##############################"
echo "############## Don't forget to turn on the SPI interface! #############"