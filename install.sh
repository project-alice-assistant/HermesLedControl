#!/usr/bin/env bash

apt-get update
apt-get install -y python-pip
apt-get install -y mosquitto
apt-get install -y mosquitto-clients
apt-get install -y python-numpy

pip install spidev
pip install gpiozero
pip install paho-mqtt
pip install pytoml

mkdir logs
chown pi logs

cp snipsledcontrol.service /etc/systemd/system
systemctl enable snipsledcontrol