#!/usr/bin/env bash

if [[ "$EUID" -ne 0 ]]
  then echo "Please run as root"
  exit
fi

apt-get install git

latest=$(curl --silent "https://api.github.com/repos/project-alice-assistant/HermesLedControl/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
dest="$HOME/HermesLedControl"

rm -rf "$dest"
git clone https://github.com/project-alice-assistant/HermesLedControl.git "$dest"
cd "$dest" || exit
git checkout "$latest"
git pull
chown -R "$(logname)" "$dest"

chmod +x install.sh
./install.sh "$latest"
