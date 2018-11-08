#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "No version supplied"
    exit
else
    VERSION=$1
fi

apt-get update
apt-get install -y python-pip
apt-get install -y mosquitto
apt-get install -y mosquitto-clients

pip install RPi.GPIO
pip install spidev
pip install gpiozero
pip install paho-mqtt
pip install pytoml

mkdir -p logs
chown pi logs
chmod +x ./installers/matrixvoice.sh

directory=${PWD##*/}

if [ ! -f /etc/systemd/system/snipsledcontrol.service ]; then
    cp snipsledcontrol.service /etc/systemd/system
fi

sed -i -e "s/snipsLedControl[0-9\.v_]*/snipsLedControl_v${VERSION}/" /etc/systemd/system/snipsledcontrol.service

systemctl daemon-reload
systemctl enable snipsledcontrol

echo "Finished installing Snips Led Control version $VERSION"
echo "You may want to copy over your custom led patterns to the new version"