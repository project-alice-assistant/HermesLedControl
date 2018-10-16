#!/usr/bin/env bash

apt-get update
apt-get install -y python-pip
apt-get install -y mosquitto
apt-get install -y mosquitto-clients

pip install spidev
pip install gpiozero
pip install paho-mqtt
pip install pytoml
pip install numpy

mkdir logs
chown _snips logs

cp snipsledcontrol.service /etc/systemd/system
systemctl enable snipsledcontrol