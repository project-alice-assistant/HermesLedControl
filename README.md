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
And if you are a private person, I can implement your hardware with your help. For that contact me. We will work it out together, over Discord. I still appreciate a beer every now and then, so feel free to refresh me: https://paypal.me/Psychokiller1888


# Installation

Download the automatic downloading tool. Do not use master unless you know what you are doing!
```
wget https://gist.githubusercontent.com/Psychokiller1888/a9826f92c5a3c5d03f34d182fda1ce4c/raw/6f31a789c95f0571b1a4e03838c63fbadd0e1d0f/slc_download.sh
```

Run it

```
sudo chmod +x slc_download.sh
sudo ./slc_download.sh
```

Of course you should have your device installed and working

Sudo is required to install as we download the missing packages and create a log directory

There's no need to edit anything


# Update

Follow the same instructions as the install


# Customize

You have to/can customize the leds, depending on what leds hardware you have. By default it is set for the 3 leds respeaker 2 with a custom pattern. To change this:

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
We all want to turn our lights off for the night. SLC does listen to the few mqtt topics Snips uses, so you don't have to do anything for it work. But, if you want to go a bit further, there's a few extra topics SLC listens to:

- **hermes/leds/toggle**: Publish on this topic to toggle the leds state. If the current state is 'off' it's toggled to 'on' and vice versa
- **hermes/leds/toggleOn**: Publish on this topic to toggle the leds to on. The onStart animation will trigger
- **hermes/leds/toggleOff**: Publish on this topic to toggle the leds to off. No more leds will light until toggled back on

Shell exemple:

```
mosquitto_pub -p 1883 -t 'hermes/leds/toggleOff' -m '{"siteId" : "default"}'
mosquitto_pub -p 1883 -t 'hermes/leds/toggleOn' -m '{"siteId" : "default"}'
```

Python exemple:

```
publish.single('hermes/leds/toggleOff', payload=json.dumps({'siteId': 'default'}), 127.0.0.1, 1883)
publish.single('hermes/leds/toggleOn', payload=json.dumps({'siteId': 'default'}), 127.0.0.1, 1883)
```

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
- --defaultBrightness: Set a default brightness for your leds, default=50
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
