#!/usr/bin/env bash

echo "######################## Matrix Voice / Creator installation ########################"
echo "######################### Please run this script with sudo ##########################"

curl https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list
echo "deb http://download.opensuse.org/repositories/network:/messaging:/zeromq:/release-stable/Debian_9.0/ ./" | sudo tee /etc/apt/sources.list.d/zeromq.list
wget https://download.opensuse.org/repositories/network:/messaging:/zeromq:/release-stable/Debian_9.0/Release.key -O- | sudo apt-key add
sudo apt-get update
sudo apt-get install -y build-essential python-dev matrixio-malos

pip --no-cache-dir install appdirs
pip --no-cache-dir install backports-abc
pip --no-cache-dir install certifi
pip --no-cache-dir install matrix_io-proto
pip --no-cache-dir install packaging
pip --no-cache-dir install protobuf
pip --no-cache-dir install pyparsing
pip --no-cache-dir install pyzmq
pip --no-cache-dir install zmq
pip --no-cache-dir install singledispatch
pip --no-cache-dir install six
pip --no-cache-dir install tornado

echo "######################## All done! ########################"
echo "##################### Enjoy! Psycho #######################"