#!/usr/bin/env bash
echo "############### Respeaker Core V2 installation ########################"
echo "############## Please run this script with sudo #######################"

USER=$1
FVENV=$2

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

sudo -u ${USER} bash <<EOF
    source ${FVENV}/bin/activate
    pip3 uninstall -y gpiozero
    pip3 uninstall -y RPi.GPIO
    pip3 --no-cache-dir install numpy
EOF

apt-get install -y python-mraa libmraa1
cp -R /usr/lib/"${PYTHON}"/dist-packages/python-mraa "${FVENV}"/lib/"${PYTHON}"/site-packages/
chown "${USER}" "${FVENV}"/lib/"${PYTHON}"/site-packages/python-mraa

echo "############################## All done! ##############################"
echo "################################ Enjoy! ###############################"
