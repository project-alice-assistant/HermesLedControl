#!/usr/bin/env bash

if [[ "$EUID" -ne 0 ]]
  then echo "Please run as root"
  exit
fi

url=$(curl --silent "https://api.github.com/repos/project-alice-assistant/HermesLedControl/releases/latest" | grep -Po '"tarball_url": "\K.*?(?=")')
latest=$(curl --silent "https://api.github.com/repos/project-alice-assistant/HermesLedControl/releases/latest" | grep -Po '"tag_name": "\K.*?(?=")')

path='/home/'$(logname)
dest=${path}/hermesLedControl_${latest}
rm ${latest}
rm -rf ${dest}
mkdir -p ${dest}

wget ${url}
tar -xzf ${latest} -C ${dest} --strip-components=1
rm ${latest}

chown -R $(logname) ${dest}
cd ${dest}
chmod +x install.sh
./install.sh ${latest}
