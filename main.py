#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime 					import datetime
import logging.handlers
import signal
import time
from models.SnipsLedControl 	import SnipsLedControl

formatter = logging.Formatter('%(asctime)s [%(threadName)s] - [%(levelname)s] - %(message)s')

_logger = logging.getLogger('SnipsLedControl')
_logger.setLevel(logging.INFO)

date = int(datetime.now().strftime('%Y%m%d'))

handler = logging.FileHandler(filename='logs.log', mode='w')
rotatingHandler = logging.handlers.RotatingFileHandler(filename='./logs/{}-logs.log'.format(date), mode='a', maxBytes=100000, backupCount=5)
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
	_logger.info('Starting Snips Led Control')

	signal.signal(signal.SIGINT, stopHandler)
	signal.signal(signal.SIGTERM, stopHandler)

	parser = argparse.ArgumentParser(prog='Snips Led Control')
	parser.add_argument('--mqttServer', help='Defines to what mqtt server SLC should connect. Overrides snips.toml', type=str)
	parser.add_argument('--mqttPort', help='Defines what port t use to connect to mqtt. Overrides snips.toml', type=str)
	parser.add_argument('--clientId', help='Defines a client id. Overrides snips.toml', type=str)
	parser.add_argument('--hardware', help='Type of hardware in use', type=str, default='respeaker2',
						choices=[
							"respeaker2",
							"respeaker4",
							"respeakerMicArrayV2",
							"neoPixels12leds",
							"matrixvoice"
						])
	parser.add_argument('--leds', help='Override the amount of leds on your hardware', type=int)
	parser.add_argument('--pattern', help='The pattern to be used by SLC (google / alexa / custom)', type=str, choices=['google', 'alexa', 'custom'], default='google')
	parser.add_argument('--offPattern', help='Define an off led pattern', type=str)
	parser.add_argument('--idlePattern', help='Define an idle led pattern', type=str)
	parser.add_argument('--wakeupPattern', help='Define a wakeup led pattern', type=str)
	parser.add_argument('--speakPattern', help='Define a speak led pattern', type=str)
	parser.add_argument('--thinkPattern', help='Define a think led pattern', type=str)
	parser.add_argument('--listenPattern', help='Define a listen led pattern', type=str)
	parser.add_argument('--errorPattern', help='Define an error led pattern', type=str)
	parser.add_argument('--successPattern', help='Define a success led pattern', type=str)
	parser.add_argument('--defaultState', help='Define if the leds should be active or not by default', type=str, choices=['on', 'off'], default='on')
	parser.add_argument('--gpioPin', help='Define the gpio pin wiring number to use when your leds use gpio', type=int)
	parser.add_argument('--vid', help='Define the vid pin wiring number to use when your leds use usb', type=str)
	parser.add_argument('--pid', help='Define the pid pin wiring number to use when your leds use usb', type=str)
	args = parser.parse_args()

	slc = SnipsLedControl(args)
	slc.onStart()

	try:
		while RUNNING:
			time.sleep(0.1)
	except KeyboardInterrupt:
		pass
	finally:
		_logger.info('Shutting down Snips Led Control')
		slc.onStop()

if __name__ == '__main__':
	RUNNING = True
	main()
