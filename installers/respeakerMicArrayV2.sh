#!/usr/bin/env bash
echo "############### Respeaker Mic Array V2 installation ########################"
echo "################ Please run this script with sudo ##########################"

USER=$1
FVENV=$2

echo "How many channels do you want to use?"
select channels in "1" "6"; do
    case "$channels" in
        *) break;;
    esac
done

sudo -u ${USER} bash <<EOF
    source ${FVENV}/bin/activate
    pip3 install click
    pip3 install pyusb
    pip3 --no-cache-dir install numpy

    cd /home/${USER}
    rm -rf /home/${USER}/usb_4_mic_array
    git clone https://github.com/respeaker/usb_4_mic_array.git
    cd usb_4_mic_array

    if [[ "$channels" == 6 ]]; then
        python3 dfu.py --download 6_channels_firmware.bin
    else
        python3 dfu.py --download 1_channel_firmware.bin
    fi
EOF

sed -i -e "s/User="${USER}"/User=root/" /etc/systemd/system/hermesledcontrol.service

echo "############################## All done! ##############################"
echo "############## Don't forget to turn on the SPI interface! #############"
