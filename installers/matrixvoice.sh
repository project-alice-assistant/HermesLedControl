#!/usr/bin/env bash

echo "######################## Matrix Voice installation ########################"
echo "#################### Please run this script with sudo #####################"

mkdir -p /home/pi/matrixvoice
cd /home/pi/matrixvoice
wget "https://github.com/matrix-io/matrix-creator-malos/blob/master/src/python_test/Pipfile" -O Pipfile
wget "https://github.com/matrix-io/matrix-creator-malos/blob/master/src/python_test/Pipfile.lock" -O Pipfile.lock
wget "https://raw.githubusercontent.com/matrix-io/matrix-creator-malos/master/src/python_test/requirements.txt" -O requirements.txt
apt-get update
apt-get install build-essential python-dev python-pip
pip install -r requirements.txt
rm -rf /home/pi/matrixvoice

echo "######################## All done! ########################"
echo "##################### Enjoy! Psycho #######################"