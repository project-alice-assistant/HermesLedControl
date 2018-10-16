#!/usr/bin/env bash

apt-get update
apt-get install -y python-pip
pip install spidev
pip install numpy
pip install gpiozero

mkdir logs
chown _snips logs

cp snipsledcontrol.service /etc/systemd/system
systemctl enable snipsledcontrol