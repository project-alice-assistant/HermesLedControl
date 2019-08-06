#!/usr/bin/env bash
echo "######################## Matrix Voice / Creator installation ########################"
echo "######################### Please run this script with sudo ##########################"

USER=$1
FVENV=$2

curl https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list
apt-get update
apt-get install -y matrixio-creator-init libmatrixio-creator-hal libmatrixio-creator-hal-dev

sudo -u ${USER} bash <<EOF
    source ${FVENV}/bin/activate
    pip3 --no-cache-dir install matrix-lite
EOF

echo "######################## All done! ########################"
echo "####### After the install is over, please reboot! #########"
echo "################## Enjoy SLC! Psycho ######################"