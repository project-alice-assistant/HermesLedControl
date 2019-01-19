#!/usr/bin/env bash
url=$(curl --silent "https://api.github.com/repos/Psychokiller1888/snipsLedControl/releases/latest" | grep -Po '"tarball_url": "\K.*?(?=")')
latest=$(curl --silent "https://api.github.com/repos/Psychokiller1888/snipsLedControl/releases/latest" | grep -Po '"tag_name": "\K.*?(?=")')

path='/home/'$(logname)
dest=$path/snipsLedControl_$latest
rm $latest
rm -rf $dest
mkdir -p $dest

wget $url
tar -xzf $latest -C $dest --strip-components=1
rm $latest

cd $dest
chmod +x install.sh
./install.sh $latest