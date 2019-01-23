#!/usr/bin/env bash

echo "############### Respeaker Mic Array V2 installation ########################"
echo "################ Please run this script with sudo ##########################"

echo "How many channels do you want to use?"
select channels in "1" "6"; do
    case $channels in
        *) break;;
    esac
done

pip install click
pip install pyusb
cd /home/pi
rm -rf /home/pi/usb_4_mic_array
git clone https://github.com/respeaker/usb_4_mic_array.git
cd usb_4_mic_array

if [ "channels" == 6 ]; then
    python dfu.py --download 6_channels_firmware.bin
else
    python dfu.py --download 1_channel_firmware.bin
fi

echo "############################## All done! ##############################"
echo "############## Don't forget to turn on the SPI interface! #############"