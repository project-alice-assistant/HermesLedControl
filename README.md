# SLC - Snips Led Control
Provides an easy way to control your leds on a Snips install.

It is reading /etc/snips.toml on start to get the mqtt server in use as well as the device's siteId. It defaults to 'localhost' and 'default' if these aren't set in snips.toml.


# Supported hardware
- Respeaker 2
- Respeaker 4
- Respeaker Mic Array V2
- NeoPixels ring
- Matrix Voice

I don't have the budget to buy every other devices just to implement them. If you are a manufacturer, **I appreciate hardware donations :-)**, they will be used wisely in my voice assistant projects.
And if you are a private person, I can implement your hardware with your help. For that contact me. We will work it out together, over Discord


# Installation

Download the latest release. Do not use master unless you know what you are doing!
```
curl https://api.github.com/repos/Psychokiller1888/snipsLedControl/releases/latest | grep "zipball_url" | sed -E 's/.*"([^"]+)".*/\1/' | wget -qi -
```

Unzip it and install! Don't forget to change the version number in the command lines

```
unzip slc_v1.0
cd slc_v1.0
sudo ./install.sh
```

Of course you should have your device installed and working

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

You have to/can customize the leds, depending on what leds hardware you have. By default it will run for the 3 leds respeaker 2 with a custom pattern. To change this:

```
sudo systemctl stop snipsledcontrol
sudo nano /etc/systemd/system/snipsledcontrol.service
```

The default ExecStart command is `ExecStart=/usr/bin/python main.py`. You can use and add as many arguments as needed here.
The full list of arguments can be found as follow:

```
cd ~
cd snipsLedControl
python main.py --help
```

Or at the end of the page

You can set the server, port, client id and others directly via arguments

You want to have a Google Home like effect on your respeaker 4? Simply change the ExecStart command to `python main.py --hardware=respeaker4 --pattern=google`

You want your own pattern? Edit snipsLedControl/ledPatterns/CustomLedPattern.py.

Dont forget to `sudo systemctl daemon-reload` if you make any changes to snipsledcontrol.service and to `sudo systemctl restart snipsledcontrol` if you made any changes to CustomLedPattern.py

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
- --hardware: Type of hardware in use, default: respeaker2, choices: respeaker2, respeaker4, respeakerMicArrayV2, neoPixels12leds, matrixvoice, default: respeaker2
- --leds: Number of leds to control, default=3
- --pattern: The pattern to be used by SLC, choices: 'google', 'alexa', 'custom', default: google
- --offListener: Allows you to define which topics will trigger the off pattern, choices: hermes/hotword/toggleOn, hermes/tts/sayFinished, hermes/audioServer/playFinished, default: hermes/hotword/toggleOn
- --offPattern: Define an off led pattern
- --idlePattern: Define an idle led pattern
- --wakeupPattern: Define a wakeup led pattern
- --speakPattern: Define a speak led pattern
- --thinkPattern: Define a think led pattern
- --listenPattern: Define a listen led pattern
- --errorPattern: Define an error led pattern
- --successPattern: Define a success led pattern
- --defaultState: Define if the leds should be active or not by default, choices: 'on', 'off', default: on
- --gpioPin: Define the gpio pin wiring number to use when your leds use gpio
- --vid: Define the vid pin wiring number to use when your leds use usb
- --pid: Define the pid pin wiring number to use when your leds use usb
- --matrixIp: [Matrix Voice] - Define the ip of your matrix voice, default: 127.0.0.1
- --everloopPort: [Matrix Voice] - Define the everloop port, default: 20021
