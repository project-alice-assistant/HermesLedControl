# SLC - Snips Led Control
Provides an easy way to control your leds on a Snips install.

It is reading /etc/snips.toml on start to get the mqtt server in use as well as the device's siteId. It defaults to 'localhost' and 'default' if these aren't set in snips.toml.


# Installation

```
sudo raspi-config

Go to Interfacing Options -> SPI and enable it

cd ~
git clone https://github.com/Psychokiller1888/snipsLedControl.git
cd snipsLedControl
sudo chmod +x install.sh
sudo ./install.sh
```

Sudo is required to install as we download the missing packages and create a log directory

There's no need to edit anything


# Update

```
cd ~
cd snipsLedControl
sudo chmod +x update.sh
sudo ./update.sh
```


# Customize

You have to/can customize the leds, depending on what respeaker you have. By default it will run for the 3 leds respeaker 2 with a Google Home assistant pattern. To change this:

```
sudo systemctl stop snipsledcontrol
sudo nano /etc/systemd/system/snipsledcontrol.service
```

The default ExecStart command is `ExecStart=/usr/bin/python main.py --pattern=google --leds=3` which means it will start main.py using google pattern and 3 leds. Change to suit your needs. As patterns you have the choice between "**google**", "**alexa**" and "**custom**".

For a full list of options:

```
cd ~
cd snipsLedControl
python main.py --help
```

You can set the server, port, client id and others directly via arguments

You want your own pattern? Set execStart to "custom" and edit snipsLedControl/ledPatterns/CustomLedPattern.py. By default it's a copy of GoogleLedPattern

Once edited do:

```
sudo systemctl daemon-reload
sudo systemctl start snipsledcontrol
```

# Special treats
We all want to turn our lights off for the night. SLC does listen to the few mqtty topics Snips uses, so you don't have to do anything for it work. But, if you want to go a bit further, there's a few extra topics SLC listens to:

- **hermes/leds/toggle**: Publish on this topic to toggle the leds state. If the current is 'off' it will change to 'on' and vice versa
- **hermes/leds/toggleOn**: Publish on this topic to toggle the leds to on. The led pattern will show
- **hermes/leds/toggleOff**: Publish on this topic to toggle the leds to off. No more leds will light until toggled back on


# Uninstall

```
sudo systemctl disable snipsledcontrol
sudo rm -rf snipsLedControl
```


# Arguments list

- --mqttServer: Defines to what mqtt server SLC should connect. Overrides snips.toml
- --mqttPort: Defines what port t use to connect to mqtt. Overrides snips.toml
- --clientId: Defines a client id. Overrides snips.toml
- --pattern: The pattern to be used by SLC, choices: 'google', 'alexa', 'custom', default: google
- --leds: Number of leds to control, default=3
- --offPattern: Define an off led pattern
- --idlePattern: Define an idle led pattern
- --wakeupPattern: Define a wakeup led pattern
- --talkPattern: Define a talk led pattern
- --thinkPattern: Define a think led pattern
- --listenPattern: Define a listen led pattern
- --errorPattern: Define an error led pattern
- --successPattern: Define a success led pattern
- --defaultState: Define if the leds should be active or not by default, choices: 'on', 'off', default: on
