#!/usr/bin/env bash

echo "############### Respeaker 7 Mic Array installation #########################"
echo "################ Please run this script with sudo ##########################"

pip uninstall -y gpiozero
pip uninstall -y RPi.GPIO

pip install respeaker

echo "############################## All done! ##############################"
echo "############## Don't forget to turn on the SPI interface! #############"