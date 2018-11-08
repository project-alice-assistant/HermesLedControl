#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "No version supplied"
    exit
else
    VERSION=$1
fi

echo "What device do you wish to control with SLC?"
select device in "respeaker2" "respeaker4" "respeakerMicArrayV2" "neopixels" "matrixvoice" "don't overwrite existing parameters" "cancel installation"; do
    case $device in
        neopixels ) device="neoPixels12leds"; break;;
        cancel ) exit;;
        *) break;;
    esac
done

if [ "$device" != "don't overwrite existing parameters" ]; then
    echo "What pattern do you want to use?"
    select pattern in "google" "alexa" "custom" "cancel installation"; do
        case $pattern in
            cancel ) exit;;
            *) break;;
        esac
    done
fi

systemctl stop snipsledcontrol

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

sed -i -e "s/snipsLedControl[0-9\.v_]*/snipsLedControl_${VERSION}/" /etc/systemd/system/snipsledcontrol.service

if [ "$device" != "don't overwrite existing parameters" ]; then
    sed -i -e "s/python main\.py.*/python main.py --hardware=${device} --pattern=${pattern}/" /etc/systemd/system/snipsledcontrol.service
fi

systemctl daemon-reload
systemctl enable snipsledcontrol
systemctl start snipsledcontrol

echo "Finished installing Snips Led Control $VERSION"
echo "You may want to copy over your custom led patterns to the new version"