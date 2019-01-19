#!/usr/bin/env bash

echo "############### Respeaker Mic Array V2 installation ########################"
echo "################ Please run this script with sudo ##########################"

echo "How many channels do you want to use?"
select channels in "1" "2" "3" "4" "5" "6"; do
    case $channels in
        *) break;;
    esac
done

apt-get install pyusb click
cd /home/pi
rm -rf /home/pi/usb_4_mic_array
git clone https://github.com/respeaker/usb_4_mic_array.git
cd usb_4_mic_array
python dfu.py --download "$channels"_channels_firmware.bin

echo "############################## All done! ##############################"
echo "############## Don't forget to turn on the SPI interface! #############"