#!/usr/bin/env bash

if [[ "$EUID" -ne 0 ]]
  then echo "Please run as root"
  exit
fi

apt-get install git

if [[ -z "$1" ]]; then
    echo "No version supplied"
    latest=$(curl --silent "https://api.github.com/repos/project-alice-assistant/HermesLedControl/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
    echo "Will download $latest"
    VERSION=$latest
else
    VERSION=$1
    echo "Supplied version $VERSION"
fi

dest="/home/$(logname)/HermesLedControl"

rm -rf "$dest"
git clone https://github.com/project-alice-assistant/HermesLedControl.git "$dest"
cd "$dest" || exit
git fetch
git checkout "$VERSION"
git pull
chown -R "$(logname)" "$dest"

chmod +x install.sh
./install.sh
