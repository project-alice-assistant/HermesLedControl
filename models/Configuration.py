import argparse
import logging
import sys
import yaml
from pathlib import Path


logger = logging.getLogger('HermesLedControl')
defaultValues = {
	'engine'           : 'projectalice',
	'pathToConfig'     : '~/ProjectAlice/config.json',
	'hardware'         : 'respeaker2Mics',
	'pattern'          : 'google',
	'offListener'      : 'hermes/hotword/toggleOn',
	'enableDoA'        : False,
	'defaultState'     : 'on',
	'matrixIp'         : '127.0.0.1',
	'defaultBrightness': 50,
	'pureGpioPinout'   : [],
	'everloopPort'     : 20021,
	'activeHigh'       : True,
	'debug'            : False,
	'timeout'          : 120
}

choices = {
	'engine'      : [
		'projectalice',
		'rhasspy'
	],
	'hardware'    : [
		'respeaker2Mics',
		'respeaker4MicArray',
		'respeakerMicArrayV2',
		'respeakerMicArrayV1',
		'respeakerCoreV2',
		'respeaker6MicArray',
		'respeaker7MicArray',
		'matrixvoice',
		'matrixcreator',
		'matrixvoiceZMQ',
		'matrixcreatorZMQ',
		'neoPixelsSK6812RGBW',
		'neoPixelsWS2812RGB',
		'googleAIY',
		'puregpio',
		'dummy'
	],
	'pattern'     : [
		'projectalice',
		'google',
		'alexa',
		'kiboost',
		'pgas',
		'fake-name',
		'custom'
	],
	'offListener' : [
		'hermes/hotword/toggleOn',
		'hermes/tts/sayFinished',
		'hermes/audioServer/playFinished'
	],
	'defaultState': [
		'on',
		'off'
	]
}


def readConfiguration() -> argparse.Namespace:
	logger.setLevel('INFO')
	logger.info('Reading command line arguments')
	args = parseArguments()

	if args.debug:
		logger.setLevel('DEBUG')

	logger.debug('Applying configuration file')
	applyConfigFile(args)
	logger.debug('Applying default values')
	applyDefaultValues(args)
	logger.debug(args)
	return args


def applyConfigFile(args: argparse.Namespace):
	path = Path(args.hermesLedControlConfig).expanduser().resolve()
	logger.info(f"Trying to load configuration from '{str(path)}'")
	if path.exists():
		try:
			with path.open('r') as configFile:
				data = yaml.load(configFile, Loader=yaml.FullLoader)
				logger.info('Configuration file read successfully')

				for key, value in data.items():
					if getattr(args, key) is None:
						if key in choices and value not in choices[key]:
							error = f"configuration option '{key}': invalid choice: '{value}' (choose from {', '.join(choices[key])})"
							logger.critical(error)
							sys.exit(error)
						setattr(args, key, value)
					else:
						logger.debug(f"'{key}' was provided as command line argument. Ignoring config file.")
		except IOError:
			logger.warning(f"Unable to read configuration file '{str(path)}'")
	else:
		logger.warning(f"Configuration file '{str(path)}' not found")


def applyDefaultValues(args: argparse.Namespace):
	for key, value in defaultValues.items():
		if getattr(args, key) is None:
			setattr(args, key, value)


def parseArguments() -> argparse.Namespace:
	parser = argparse.ArgumentParser(prog='Hermes Led Control')
	parser.add_argument(
		'--engine',
		help='What assistant engine are you using?',
		type=str,
		choices=choices['engine']
	)
	parser.add_argument(
		'--pathToConfig',
		help='Defines where the mqtt configuration file is to be found',
		type=str
	)
	parser.add_argument(
		'--mqttServer',
		help='Defines to what mqtt server SLC should connect. Overrides any config file',
		type=str
	)
	parser.add_argument(
		'--mqttPort',
		help='Defines what port to use to connect to mqtt. Overrides any config file',
		type=str
	)
	parser.add_argument(
		'--mqttUsername',
		help='Mqtt username if required. Overrides any config file',
		type=str
	)
	parser.add_argument(
		'--mqttPassword',
		help='Mqtt password if required. Overrides any config file',
		type=str
	)
	parser.add_argument(
		'--clientId',
		help='Defines a client id. Overrides any config file',
		type=str
	)
	parser.add_argument(
		'--hardware',
		help='Type of hardware in use',
		type=str,
		choices=choices['hardware']
	)
	parser.add_argument(
		'--leds',
		help='Override the amount of leds on your hardware',
		type=int
	)
	parser.add_argument(
		'--defaultBrightness',
		help='Set a default brightness for your leds',
		type=int
	)
	parser.add_argument(
		'--endFrame',
		help='Respeakers, or apa102 led systems need an end frame. If your device is not working try either 255 or 0',
		type=int
	)
	parser.add_argument(
		'--pattern',
		help='The pattern to be used',
		type=str,
		choices=choices['pattern']
	)
	parser.add_argument(
		'--offListener',
		help='Allows you to define which topics will trigger the off pattern',
		type=str,
		choices=choices['offListener']
	)
	parser.add_argument(
		'--enableDoA',
		help='Enables sound direction of arrival on hardware capable of it. Resources greedy!',
		type=bool
	)
	parser.add_argument(
		'--startPattern',
		help='Define a program start led pattern',
		type=str
	)
	parser.add_argument(
		'--stopPattern',
		help='Define a prorgam stop led pattern',
		type=str
	)
	parser.add_argument(
		'--offPattern',
		help='Define an off led pattern',
		type=str
	)
	parser.add_argument(
		'--idlePattern',
		help='Define an idle led pattern',
		type=str
	)
	parser.add_argument(
		'--wakeupPattern',
		help='Define a wakeup led pattern',
		type=str
	)
	parser.add_argument(
		'--speakPattern',
		help='Define a speak led pattern',
		type=str
	)
	parser.add_argument(
		'--thinkPattern',
		help='Define a think led pattern',
		type=str
	)
	parser.add_argument(
		'--listenPattern',
		help='Define a listen led pattern',
		type=str
	)
	parser.add_argument(
		'--errorPattern',
		help='Define an error led pattern',
		type=str
	)
	parser.add_argument(
		'--successPattern',
		help='Define a success led pattern',
		type=str
	)
	parser.add_argument(
		'--updatingPattern',
		help='Define an updating led pattern',
		type=str
	)
	parser.add_argument(
		'--callPattern',
		help='Define a call led pattern',
		type=str
	)
	parser.add_argument(
		'--setupModePattern',
		help='Define a setup mode led pattern',
		type=str
	)
	parser.add_argument(
		'--conErrorPattern',
		help='Define a connection error led pattern',
		type=str
	)
	parser.add_argument(
		'--messagePattern',
		help='Define a message led pattern',
		type=str
	)
	parser.add_argument(
		'--dndPattern',
		help='Define a do not disturb led pattern',
		type=str
	)
	parser.add_argument(
		'--defaultState',
		help='Define if the leds should be active or not by default',
		type=str,
		choices=choices['defaultState']
	)
	parser.add_argument(
		'--gpioPin',
		help='Define the gpio pin wiring number to use when your leds use gpio',
		type=int
	)
	parser.add_argument(
		'--vid',
		help='Define the vid pin wiring number to use when your leds use usb',
		type=str
	)
	parser.add_argument(
		'--pid',
		help='Define the pid pin wiring number to use when your leds use usb',
		type=str
	)
	parser.add_argument(
		'--matrixIp',
		help='[Matrix Voice] - Define the ip of your matrix voice',
		type=str
	)
	parser.add_argument(
		'--everloopPort',
		help='[Matrix Voice] - Define the everloop port',
		type=int
	)
	parser.add_argument(
		'--pureGpioPinout',
		help='[Pure GPIO] - Define the broadcom gpio number of your leds, in the order you want them',
		type=list,
		default=[]
	)
	parser.add_argument(
		'--activeHigh',
		help='[Pure GPIO] - Define how your leds are controlled',
		type=bool
	)
	parser.add_argument(
		'--timeout',
		help='Animation timeout in seconds. After the specified time without animation change this will transition to idle. Defaults to 120 seconds. Use 0 or negative values to disable.',
		type=int
	)
	parser.add_argument(
		'--hermesLedControlConfig',
		help='Define the configuration.yml file location for hermes led control',
		type=str,
		default='~/.config/HermesLedControl/configuration.yml'
	)
	parser.add_argument(
		'--debug',
		help='Enable the debug mode for the console to return more information',
		type=bool
	)
	args = parser.parse_args()

	return args
