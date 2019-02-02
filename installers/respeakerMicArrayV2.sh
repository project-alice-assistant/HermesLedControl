#!/usr/bin/env bash

echo "############### Respeaker Mic Array V2 installation ########################"
echo "################ Please run this script with sudo ##########################"

USER=$(logname)

echo "How many channels do you want to use?"
select channels in "1" "6"; do
    case $channels in
        *) break;;
    esac
done

pip install click
pip install pyusb
systemctl is-active -q pixel_ring_server && systemctl stop pixel_ring_server
pip uninstall -y pixel_ring
cd /home/$USER
rm -rf /home/$USER/usb_4_mic_array
git clone https://github.com/respeaker/usb_4_mic_array.git
cd usb_4_mic_array

if [ "channels" == 6 ]; then
    python dfu.py --download 6_channels_firmware.bin
else
    python dfu.py --download 1_channel_firmware.bin
fi

echo "############################## All done! ##############################"
echo "############## Don't forget to turn on the SPI interface! #############"