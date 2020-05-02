import argparse
import logging
from logging import handlers
import signal
import time
from datetime import datetime

from models.HermesLedControl import HermesLedControl

formatter = logging.Formatter('%(asctime)s [%(threadName)s] - [%(levelname)s] - %(message)s')

_logger = logging.getLogger('HermesLedControl')

_logger.setLevel(logging.DEBUG)

date = int(datetime.now().strftime('%Y%m%d'))

handler = logging.FileHandler(filename='logs.log', mode='w')
rotatingHandler = handlers.RotatingFileHandler(filename='./logs/{}-logs.log'.format(date), mode='a', maxBytes=100000, backupCount=5)
streamHandler = logging.StreamHandler()

handler.setFormatter(formatter)
rotatingHandler.setFormatter(formatter)

_logger.addHandler(handler)
_logger.addHandler(rotatingHandler)
_logger.addHandler(streamHandler)


def stopHandler(signum, frame):
	onStop()


def onStop():
	global RUNNING
	RUNNING = False


def main():
	_logger.info('Starting Hermes Led Control v. 2.0.6')

	signal.signal(signal.SIGINT, stopHandler)
	signal.signal(signal.SIGTERM, stopHandler)

	parser = argparse.ArgumentParser(prog='Hermes Led Control')
	parser.add_argument('--engine', help='What assistant engine are you using?', type=str, default='projectalice', choices= [
		"projectalice",
		"rhasspy",
		"snips"
	])
	parser.add_argument('--pathToConfig', help='Defines where the mqtt configuration file is to be found', type=str, default='/etc/snips.toml')
	parser.add_argument('--mqttServer', help='Defines to what mqtt server SLC should connect. Overrides any config file', type=str)
	parser.add_argument('--mqttPort', help='Defines what port to use to connect to mqtt. Overrides any config file', type=str)
	parser.add_argument('--mqttUsername', help='Mqtt username if required. Overrides any config file', type=str)
	parser.add_argument('--mqttPassword', help='Mqtt password if required. Overrides any config file', type=str)
	parser.add_argument('--clientId', help='Defines a client id. Overrides any config file', type=str)
	parser.add_argument('--hardware', help='Type of hardware in use', type=str, default='respeaker2',
						choices=[
							"respeaker2",
							"respeaker4",
							"respeakerMicArrayV2",
							"respeakerMicArrayV1",
							"respeakerCoreV2",
							"respeaker6MicArray",
							"respeaker7MicArray",
							"matrixvoice",
							"matrixcreator",
							"neoPixelsSK6812RGBW",
							"neoPixelsWS2812RGB",
							"googleAIY",
							"puregpio"
						])
	parser.add_argument('--leds', help='Override the amount of leds on your hardware', type=int)
	parser.add_argument('--defaultBrightness', help='Set a default brightness for your leds', type=int, default=50)
	parser.add_argument('--endFrame', help='Respeakers, or apa102 led systems need an end frame. If your device is not working try either 255 or 0', type=int)
	parser.add_argument('--pattern', help='The pattern to be used', type=str, default='google',
						choices=[
							'google',
							'alexa',
							'kiboost',
							'projectalice',
							'pgas',
							'custom'
						])
	parser.add_argument('--offListener', help='Allows you to define which topics will trigger the off pattern', type=str, default='hermes/hotword/toggleOn',
						choices=[
							'hermes/hotword/toggleOn',
							'hermes/tts/sayFinished',
							'hermes/audioServer/playFinished'
						])
	parser.add_argument('--enableDoA', help='Enables sound direction of arrival on hardware capable of it. Resources greedy!', type=bool, default=False)
	parser.add_argument('--startPattern', help='Define a program start led pattern', type=str)
	parser.add_argument('--stopPattern', help='Define a prorgam stop led pattern', type=str)
	parser.add_argument('--offPattern', help='Define an off led pattern', type=str)
	parser.add_argument('--idlePattern', help='Define an idle led pattern', type=str)
	parser.add_argument('--wakeupPattern', help='Define a wakeup led pattern', type=str)
	parser.add_argument('--speakPattern', help='Define a speak led pattern', type=str)
	parser.add_argument('--thinkPattern', help='Define a think led pattern', type=str)
	parser.add_argument('--listenPattern', help='Define a listen led pattern', type=str)
	parser.add_argument('--errorPattern', help='Define an error led pattern', type=str)
	parser.add_argument('--successPattern', help='Define a success led pattern', type=str)
	parser.add_argument('--updatingPattern', help='Define an updating led pattern', type=str)
	parser.add_argument('--callPattern', help='Define a call led pattern', type=str)
	parser.add_argument('--setupModePattern', help='Define a setup mode led pattern', type=str)
	parser.add_argument('--conErrorPattern', help='Define a connection error led pattern', type=str)
	parser.add_argument('--messagePattern', help='Define a message led pattern', type=str)
	parser.add_argument('--dndPattern', help='Define a do not disturb led pattern', type=str)
	parser.add_argument('--defaultState', help='Define if the leds should be active or not by default', type=str, choices=['on', 'off'], default='on')
	parser.add_argument('--gpioPin', help='Define the gpio pin wiring number to use when your leds use gpio', type=int)
	parser.add_argument('--vid', help='Define the vid pin wiring number to use when your leds use usb', type=str)
	parser.add_argument('--pid', help='Define the pid pin wiring number to use when your leds use usb', type=str)
	parser.add_argument('--matrixIp', help='[Matrix Voice] - Define the ip of your matrix voice', type=str, default='127.0.0.1')
	parser.add_argument('--everloopPort', help='[Matrix Voice] - Define the everloop port', type=int, default=20021)
	parser.add_argument('--pureGpioPinout', help='[Pure GPIO] - Define the broadcom gpio number of your leds, in the order you want them', type=list, default=[])
	parser.add_argument('--activeHigh', help='[Pure GPIO] - Define how your leds are controlled', type=bool, default=True)
	parser.add_argument('--debug', help='Enable the debug mode for the console to return more informations', type=bool, default=False)
	args = parser.parse_args()

	slc = HermesLedControl(args)
	slc.onStart()

	try:
		while RUNNING:
			time.sleep(0.1)
	except KeyboardInterrupt:
		pass
	finally:
		_logger.info('Shutting down Hermes Led Control')
		slc.onStop()


if __name__ == '__main__':
	RUNNING = True
	main()
