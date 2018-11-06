#!/usr/bin/env bash

print "######################## Matrix Voice installation ########################"
print "#################### Please run this script with sudo #####################"

cd ~
mkdir matrixvoice
cd matrixvoice
wget "https://github.com/matrix-io/matrix-creator-malos/blob/master/src/python_test/Pipfile" -O Pipfile
wget "https://github.com/matrix-io/matrix-creator-malos/blob/master/src/python_test/Pipfile.lock" -O Pipfile.lock
wget "https://raw.githubusercontent.com/matrix-io/matrix-creator-malos/master/src/python_test/requirements.txt" -O requirements.txt
apt-get update
apt-get install build-essential python-dev python-pip
pip install -r requirements.txt
cd ~
rm -rf matrixvoice

print "######################## All done! ########################"
print "##################### Enjoy! Psycho #######################"