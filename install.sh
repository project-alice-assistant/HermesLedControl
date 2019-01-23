#!/usr/bin/env bash

if [ -z "$1" ]; then
    echo "No version supplied"
    exit
else
    VERSION=$1
fi

echo "What device do you wish to control with SLC?"
select device in "respeaker2" "respeaker4" "respeakerMicArrayV2" "neoPixelsSK6812RGBW" "neoPixelsWS2812RGB" "matrixvoice" "matrixcreator" "respeakerCoreV2" "respeaker6MicArray" "googleAIY" "I'm using simple leds on GPIOs" "don't overwrite existing parameters" "cancel"; do
    case $device in
        cancel) exit;;
        *) break;;
    esac
done

if [ "$device" != "don't overwrite existing parameters" ]; then
    echo "What pattern do you want to use?"
    select pattern in "google" "alexa" "custom" "cancel"; do
        case $pattern in
            cancel) exit;;
            *) break;;
        esac
    done
fi

systemctl stop snipsledcontrol

apt-get update
apt-get install -y python-pip
apt-get install -y git
apt-get install -y mosquitto-clients
apt-get install -y portaudio19-dev
apt-get install -y python-numpy

pip --no-cache-dir install RPi.GPIO
pip --no-cache-dir install spidev
pip --no-cache-dir install gpiozero
pip --no-cache-dir install paho-mqtt
pip --no-cache-dir install pytoml

mkdir -p logs
chown pi logs

chmod +x ./installers/matrixVoiceCreator.sh
chmod +x ./installers/neopixels.sh
chmod +x ./installers/respeakerCoreV2.sh
chmod +x ./installers/respeakerMicArrayV2.sh
chmod +x ./installers/respeakers.sh

directory=${PWD##*/}

if [ ! -f /etc/systemd/system/snipsledcontrol.service ]; then
    cp snipsledcontrol.service /etc/systemd/system
fi

sed -i -e "s/snipsLedControl[0-9\.v_]*/snipsLedControl_${VERSION}/" /etc/systemd/system/snipsledcontrol.service

if [ "$device" != "don't overwrite existing parameters" ]; then
    sed -i -e "s/python main\.py.*/python main.py --hardware=${device} --pattern=${pattern}/" /etc/systemd/system/snipsledcontrol.service
fi

if [[ -d "/var/lib/snips/skills/snips-skill-respeaker" ]]; then
    echo "snips-skill-respeaker detected, do you want to remove it? Leaving it be might result in weird behaviors..."
    select answer in "yes" "no" "cancel"; do
        case $answer in
            yes)
                rm -rf "/var/lib/snips/skills/snips-skill-respeaker"
                systemctl restart snips-*
                echo "Removed snips-skill-respeaker"
                break;;
            cancel) exit;;
            *) break;;
        esac
    done
fi

echo "Do you need to install / configure your $device?"
select answer in "yes" "no" "cancel"; do
    case $answer in
        yes)
            case $device in
                matrixvoice)
                    chmod +x ./installers/matrixVoiceCreator.sh
                    ./installers/matrixVoiceCreator.sh
                    break
                    ;;
                matrixcreator)
                    chmod +x ./installers/matrixVoiceCreator.sh
                    ./installers/matrixVoiceCreator.sh
                    break
                    ;;
                respeaker2)
                    chmod +x ./installers/respeakers.sh
                    ./installers/respeakers.sh
                    break
                    ;;
                respeaker4)
                    chmod +x ./installers/respeakers.sh
                    ./installers/respeakers.sh
                    break
                    ;;
                neoPixelsSK6812RGBW)
                    chmod +x ./installers/neopixels.sh
                    ./installers/neopixels.sh
                    break
                    ;;
                neoPixelsWS2812RGB)
                    chmod +x ./installers/neopixels.sh
                    ./installers/neopixels.sh
                    break
                    ;;
                respeakerMicArrayV2)
                    chmod +x ./installers/respeakerMicArrayV2.sh
                    ./installers/respeakerMicArrayV2.sh
                    break
                    ;;
                respeakerCoreV2)
                    chmod +x ./installers/respeakerCoreV2.sh
                    ./installers/respeakerCoreV2.sh
                    break
                    ;;
                *)
                    echo "No installation needed / Installation not yet supported"
                    break
                    ;;
            esac
            break;;
        cancel) exit;;
        *) break;;
    esac
done

systemctl daemon-reload
systemctl enable snipsledcontrol
systemctl start snipsledcontrol

echo "Finished installing Snips Led Control $VERSION"
echo "You may want to copy over your custom led patterns to the new version"