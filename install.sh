#!/usr/bin/env bash

apt-get update
apt-get install -y python3-pip
apt-get install -y mosquitto
apt-get install -y mosquitto-clients

pip3 install RPi.GPIO
pip3 install spidev
pip3 install gpiozero
pip3 install paho-mqtt
pip3 install pytoml

mkdir logs
chown pi logs

cp snipsledcontrol.service /etc/systemd/system
systemctl daemon-reload
systemctl enable snipsledcontrol