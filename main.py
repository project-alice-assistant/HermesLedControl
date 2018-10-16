#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime 					import datetime
import logging.handlers
import signal
import time
from models.SnipsLedControl 	import SnipsLedControl
import sys

formatter = logging.Formatter('%(asctime)s [%(threadName)s] - [%(levelname)s] - %(message)s')

_logger = logging.getLogger('SnipsLedControl')
_logger.setLevel(logging.INFO)

date = int(datetime.now().strftime('%Y%m%d%H%M'))

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

	pattern = 'google'
	pixels = 12

	try:
		pattern = sys.argv[0]
		pixels = sys.argv[1]
	except:
		pass

	slc = SnipsLedControl(pattern=pattern, pixels=pixels)

	while RUNNING:
		time.sleep(0.1)

	_logger.info('Shutting down Snips Led Control')
	slc.onStop()

if __name__ == '__main__':
	RUNNING = True
	main()
