#!/usr/bin/env bash

echo "############### Respeaker Core V2 installation ########################"
echo "############## Please run this script with sudo #######################"

if [[ -d "/var/lib/snips/skills/snips-skill-respeaker" ]]; then
    echo "snips-skill-respeaker detected, do you want to remove it? Leaving it be might result in weird behaviors..."
    select answer in "yes" "no" "cancel"; do
        case $answer in
            yes)
                rm -rf "/var/lib/snips/skills/snips-skill-respeaker"
                systemctl restart snips-*
                echo "Removed snips-skill-respeaker"
                break;;
            cancel) exit;;
            *) break;;
        esac
    done
fi

pip uninstall -y gpiozero

echo "############################## All done! ##############################"
echo "############## Don't forget to turn on the SPI interface! #############"