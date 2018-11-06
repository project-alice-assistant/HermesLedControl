#!/usr/bin/env bash

apt-get update
apt-get install -y python-pip
apt-get install -y mosquitto
apt-get install -y mosquitto-clients

pip install RPi.GPIO
pip install spidev
pip install gpiozero
pip install paho-mqtt
pip install pytoml

mkdir logs
chown pi logs

chown +x ./installers/matrixvoice.sh

cp snipsledcontrol.service /etc/systemd/system
systemctl daemon-reload
systemctl enable snipsledcontrol