#!/usr/bin/env bash

if [[ "$EUID" -ne 0 ]]; then
    echo "Please run as root"
    exit
fi

VENV=venv

PYTHON=$(command -v python3.9)
if [[ -z "$PYTHON" ]]; then
    PYTHON=$(command -v python3.8)
    if [[ -z "$PYTHON" ]]; then
        PYTHON=$(command -v python3.7)
        if [[ -z "$PYTHON" ]]; then
            echo "Please make sure to have python 3.7 at least"
            exit
        fi
    fi
fi

USER=$(logname)
USERDIR='/home/'${USER}

echo "What assistant engine are you using?"
select engine in "projectalice" "rhasspy" "cancel"; do
    case "$engine" in
        cancel) exit;;
        *) break;;
    esac
done

if [[ "$engine" == 'rhasspy' ]]; then
    defaultPath='/.config/rhasspy/profiles/en/profile.json'
else
    defaultPath="$USERDIR/ProjectAlice/config.json"
fi

pathToAssistantConfig=defaultPath
echo "What's the path to your assistant config file?"
read -p "Path: (${defaultPath})" pathToAssistantConfig
echo "Path: $pathToAssistantConfig"
pathToAssistantConfig=${pathToAssistantConfig//\//\\/}

echo "What device do you wish to control with SLC?"
select device in "respeaker2Mics" "respeaker4MicArray" "respeakerMicArrayV2" "respeakerMicArrayV1" "neoPixelsSK6812RGBW" "neoPixelsWS2812RGB" "matrixvoice" "matrixcreator" "matrixvoiceZMQ" "matrixcreatorZMQ" "respeakerCoreV2" "respeaker6MicArray" "respeaker7MicArray" "googleAIY" "I'm using simple leds on GPIOs" "don't overwrite existing parameters" "cancel"; do
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
    select pattern in "projectalice" "google" "alexa" "pgas" "kiboost" "fake-name" "custom" "cancel"; do
        case "$pattern" in
            cancel) exit;;
            *) break;;
        esac
    done

	defaultConfigurationPath=${USERDIR}'/.config/HermesLedControl'
	echo "Where should the configuration be saved to?"
	read -p "Path (${defaultConfigurationPath})" configurationPath
	configurationPath=${configurationPath:-$defaultConfigurationPath}
	configurationFile=${configurationPath}/configuration.yml
	echo "Path: $configurationPath"
	escapedConfigurationFile=${configurationFile//\//\\/}
fi

doaConfigValue="false"
if [[ "$device" == "respeaker4MicArray" || "$device" == "respeakerMicArrayV2" || "$device" == "respeakerMicArrayV1" || "$device" == "respeaker6MicArray" || "$device" == "respeakerCoreV2" ]]; then
	echo "Your device supports Direction of Arrival (DoA). Do you want to enable DoA now?"
	select enableDoA in "yes" "no" "install dependencies only" "cancel"; do
		case "$enableDoA" in
			"yes") doaConfigValue="true";&
			"install dependencies only")
				apt-get update
				apt-get install -y libatlas-base-dev
				break;;
			cancel) exit;;
			*) break;;
		esac
	done
fi

systemctl is-active -q hermesledcontrol && systemctl stop hermesledcontrol

apt-get update
apt-get install -y git mosquitto mosquitto-clients portaudio19-dev python3-numpy

FVENV=${USERDIR}'/HermesLedControl/'${VENV}

apt-get install -y python3-pip

if [[ -d "$FVENV" ]]; then
    rm -rf "${FVENV}"
fi

systemctl is-active -q pixel_ring_server && systemctl disable pixel_ring_server

chown -R "${USER}" "${USERDIR}/HermesLedControl"

pip3 install virtualenv
pip3 uninstall -y pixel_ring

sudo -u "${USER}" bash <<EOF
    virtualenv -p ${PYTHON} ${FVENV}
    source ${FVENV}/bin/activate
    pip install https://www.piwheels.org/simple/numpy/numpy-1.21.4-cp39-cp39-linux_armv7l.whl
    pip install -r requirements.txt --no-cache-dir
EOF

mkdir -p logs
chown "${USER}" logs

if [[ "$device" != "don't overwrite existing parameters" && -f /etc/systemd/system/hermesledcontrol.service ]]; then
    rm /etc/systemd/system/hermesledcontrol.service
fi

if [[ ! -f /etc/systemd/system/hermesledcontrol.service ]]; then
    cp hermesledcontrol.service /etc/systemd/system
fi

if [[ "$device" != "don't overwrite existing parameters" && -f ${configurationFile} ]]; then
    rm "${configurationFile}"
fi

if [[ "$device" != "don't overwrite existing parameters" && ! -f ${configurationFile} ]]; then
	mkdir -p "${configurationPath}"
    cp configuration.yml "${configurationPath}"
	chown "${USER}" "${configurationFile}"

	sed -i -e "s/%ENGINE%/${engine}/" "${configurationFile}"
	sed -i -e "s/%PATHTOCONFIG%/${pathToAssistantConfig}/" "${configurationFile}"
	sed -i -e "s/%DEVICE%/${device}/" "${configurationFile}"
	sed -i -e "s/%PATTERN%/${pattern}/" "${configurationFile}"
	sed -i -e "s/%DOA%/${doaConfigValue}/" "${configurationFile}"
fi

escaped=${USERDIR//\//\\/}
sed -i -e "s/%WORKING_DIR%/${escaped}\/HermesLedControl/" /etc/systemd/system/hermesledcontrol.service
sed -i -e "s/%USER%/${USER}/" /etc/systemd/system/hermesledcontrol.service

if [[ "$device" != "don't overwrite existing parameters" ]]; then
    sed -i -e "s/%EXECSTART%/${escaped}\/HermesLedControl\/venv\/bin\/python main.py --hermesLedControlConfig=${escapedConfigurationFile}/" /etc/systemd/system/hermesledcontrol.service
fi

echo "Do you need to install / configure your \"${device}\"? This is strongly suggested as it does turn off services that might conflict as well!"
select answer in "yes" "no" "cancel"; do
    case "$answer" in
        yes)
            case "$device" in
                matrixvoice)
                matrixcreator)
                    ./installers/matrixVoiceCreator.sh "${USER}" "${FVENV}"
                    break
                    ;;
                matrixvoiceZMQ)
                matrixcreatorZMQ)
                    ./installers/matrixCore.sh "${USER}" "${FVENV}"
                    break
                    ;;
                respeaker2Mics)
                    ./installers/respeakers.sh "${USER}" "${FVENV}"
                    break
                    ;;
                respeaker4MicArray)
                    ./installers/respeakers.sh "${USER}" "${FVENV}"
                    break
                    ;;
                respeaker6MicArray)
                    ./installers/respeakers.sh "${USER}" "${FVENV}"
                    break
                    ;;
                neoPixelsSK6812RGBW)
                    ./installers/neopixels.sh "${USER}" "${FVENV}"
                    break
                    ;;
                neoPixelsWS2812RGB)
                    ./installers/neopixels.sh "${USER}" "${FVENV}"
                    break
                    ;;
                respeakerMicArrayV2)
                    ./installers/respeakerMicArrayV2.sh "${USER}" "${FVENV}"
                    break
                    ;;
                respeakerMicArrayV1)
                    ./installers/respeakerMicArrayV1.sh "${USER}" "${FVENV}"
                    break
                    ;;
                respeakerCoreV2)
                    ./installers/respeakerCoreV2.sh "${USER}" "${FVENV}"
                    break
                    ;;
                respeaker7MicArray)
                    ./installers/respeaker7MicArray.sh "${USER}" "${FVENV}"
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

chown -R "${USER}" "${USERDIR}/HermesLedControl"

systemctl daemon-reload
systemctl enable hermesledcontrol
systemctl start hermesledcontrol

echo "Finished installing Hermes Led Control"
echo "You may want to copy over your custom led patterns to the new version"
