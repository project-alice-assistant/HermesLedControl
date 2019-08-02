#!/usr/bin/env bash

if [[ "$EUID" -ne 0 ]]; then
    echo "Please run as root"
    exit
fi

VENV=venv

PYTHON=$(command -v python3.7)
if [[ -z "$PYTHON" ]]; then
    PYTHON=$(command -v python3.6)
    if [[ -z "$PYTHON" ]]; then
        PYTHON=$(command -v python3.5)
        if [[ -z "$PYTHON" ]]; then
            echo "Please make sur to have python 3.5 at least"
            exit
        fi
    fi
fi

if [[ -z "$1" ]]; then
    echo "No version supplied"
    exit
else
    VERSION=$1
fi

USER=$(logname)
USERDIR='/home/'${USER}

echo "What device do you wish to control with SLC?"
select device in "respeaker2" "respeaker4" "respeakerMicArrayV2" "neoPixelsSK6812RGBW" "neoPixelsWS2812RGB" "matrixvoice" "matrixcreator" "respeakerCoreV2" "respeaker6MicArray" "respeaker7MicArray" "googleAIY" "I'm using simple leds on GPIOs" "don't overwrite existing parameters" "cancel"; do
    case "$device" in
        "I'm using simple leds on GPIOs")
            device=puregpio
            break;;
        cancel) exit;;
        *) break;;
    esac
done

if [[ "$device" != "don't overwrite existing parameters" ]]; then
    echo "What pattern do you want to use?"
    select pattern in "google" "alexa" "projectalice" "custom" "kiboost" "cancel"; do
        case "$pattern" in
            cancel) exit;;
            *) break;;
        esac
    done
fi

systemctl is-active -q snipsledcontrol && systemctl stop snipsledcontrol

apt-get update
apt-get install -y git mosquitto mosquitto-clients portaudio19-dev numpy

FVENV=${USERDIR}'/snipsLedControl_'${VERSION}'/'${VENV}

apt-get install -y python3-pip

if [[ -d "$FVENV" ]]; then
    rm -rf ${FVENV}
fi

systemctl is-active -q pixel_ring_server && systemctl disable pixel_ring_server

sudo -u ${USER} bash <<EOF
    pip3 install virtualenv
    virtualenv -p ${PYTHON} ${FVENV}
    source ${FVENV}/bin/activate

    pip3 --no-cache-dir install RPi.GPIO
    pip3 --no-cache-dir install spidev
    pip3 --no-cache-dir install gpiozero
    pip3 --no-cache-dir install paho-mqtt
    pip3 --no-cache-dir install toml
    pip3 uninstall -y pixel_ring
EOF

pip3 uninstall -y pixel_ring

mkdir -p logs
chown ${USER} logs

if [[ "$device" != "don't overwrite existing parameters" && -f /etc/systemd/system/snipsledcontrol.service ]]; then
    rm /etc/systemd/system/snipsledcontrol.service
fi

if [[ ! -f /etc/systemd/system/snipsledcontrol.service ]]; then
    cp snipsledcontrol.service /etc/systemd/system
fi

escaped=${USERDIR//\//\\/}
sed -i -e "s/%WORKING_DIR%/"${escaped}"\/snipsLedControl_"${VERSION}"/" /etc/systemd/system/snipsledcontrol.service
sed -i -e "s/%USER%/"${USER}"/" /etc/systemd/system/snipsledcontrol.service

if [[ "$device" != "don't overwrite existing parameters" ]]; then
    sed -i -e "s/%EXECSTART%/"${escaped}"\/snipsLedControl_"${VERSION}"\/venv\/bin\/python3 main.py --hardware="${device}" --pattern="${pattern}"/" /etc/systemd/system/snipsledcontrol.service
fi

if [[ -d "/var/lib/snips/skills/snips-skill-respeaker" ]]; then
    echo "snips-skill-respeaker detected, do you want to remove it? Leaving it be might result in weird behaviors..."
    select answer in "yes" "no" "cancel"; do
        case "$answer" in
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

echo "Do you need to install / configure your "${device}"? This is strongly suggested as it does turn off services that might conflict as well!"
select answer in "yes" "no" "cancel"; do
    case "$answer" in
        yes)
            case "$device" in
                matrixvoice)
                    chmod +x ./installers/matrixVoiceCreator.sh
                    ./installers/matrixVoiceCreator.sh USER FVENV
                    break
                    ;;
                matrixcreator)
                    chmod +x ./installers/matrixVoiceCreator.sh
                    ./installers/matrixVoiceCreator.sh USER FVENV
                    break
                    ;;
                respeaker2)
                    chmod +x ./installers/respeakers.sh USER FVENV
                    ./installers/respeakers.sh
                    break
                    ;;
                respeaker4)
                    chmod +x ./installers/respeakers.sh USER FVENV
                    ./installers/respeakers.sh
                    break
                    ;;
                respeaker6MicArray)
                    chmod +x ./installers/respeakers.sh USER FVENV
                    ./installers/respeakers.sh
                    break
                    ;;
                neoPixelsSK6812RGBW)
                    chmod +x ./installers/neopixels.sh USER FVENV
                    ./installers/neopixels.sh
                    break
                    ;;
                neoPixelsWS2812RGB)
                    chmod +x ./installers/neopixels.sh USER FVENV
                    ./installers/neopixels.sh
                    break
                    ;;
                respeakerMicArrayV2)
                    chmod +x ./installers/respeakerMicArrayV2.sh USER FVENV
                    ./installers/respeakerMicArrayV2.sh
                    break
                    ;;
                respeakerCoreV2)
                    chmod +x ./installers/respeakerCoreV2.sh USER FVENV
                    ./installers/respeakerCoreV2.sh
                    break
                    ;;
                respeaker7MicArray)
                    chmod +x ./installers/respeaker7MicArray.sh USER FVENV
                    ./installers/respeaker7MicArray.sh
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

chown -R ${USER} ${USERDIR}/snipsLedControl_${VERSION}

systemctl daemon-reload
systemctl enable snipsledcontrol
systemctl start snipsledcontrol

echo "Finished installing Snips Led Control "${VERSION}
echo "You may want to copy over your custom led patterns to the new version"