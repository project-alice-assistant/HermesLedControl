#!/usr/bin/env bash

echo "############### Respeaker 7 Mic Array installation #########################"
echo "################ Please run this script with sudo ##########################"

systemctl is-active -q pixel_ring_server && systemctl stop pixel_ring_server
pip uninstall -y pixel_ring
pip uninstall -y gpiozero
pip uninstall -y RPi.GPIO

pip install respeaker

echo "############################## All done! ##############################"
echo "############## Don't forget to turn on the SPI interface! #############"