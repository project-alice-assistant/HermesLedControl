# Work in progress, report if any problems


# snipsLedControl
Provides an easy way to control your leds on a Snips install
It is reading /etc/snips.toml on start to get the mqtt server in use as well as the device's siteId. It defaults to 'localhost' and 'default' if these aren't set in snips.toml


# Installation

```
git clone https://github.com/Psychokiller1888/snipsLedControl.git
cd snipsLedControl
sudo chmod +x install.sh
sudo install.sh
```

Sudo is required to install as we download the missing packages and create a log directory

# Customize

You have to/can customize the leds, depending on what respeaker you have. By default it will run for the 3 leds respeaker 2 with a Google Home assistant pattern. To change this:

```
sudo nano systemctl stop snipsledcontrol
sudo nano /etc/systemd/system/snipsledcontrol.service
```

The default ExecStart command is `ExecStart=/usr/bin/python main.py google 3` which means it will start main.py using google pattern and 3 leds. Change to suit your needs. As patterns you have the choice between "**google**", "**alexa**" and "**custom**".

You want your own pattern? Set execStart to "custom" and edit snipsLedControl/ledPatterns/CustomLedPattern.py. By default it's a copy of GoogleLedPattern

Once edited do:

```
sudo systemctl daemon-reload
sudo systemctl start snipsledcontrol
```
