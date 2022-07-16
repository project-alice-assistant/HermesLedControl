from logging import handlers

import logging
import signal
import time
from datetime import datetime

from models.Configuration import readConfiguration
from models.HermesLedControl import HermesLedControl


formatter = logging.Formatter('%(asctime)s [%(threadName)s] - [%(levelname)s] - %(message)s')

_logger = logging.getLogger('HermesLedControl')

_logger.setLevel(logging.DEBUG)

date = int(datetime.now().strftime('%Y%m%d'))

handler = logging.FileHandler(filename='logs.log', mode='w')
rotatingHandler = handlers.RotatingFileHandler(filename=f'./logs/{date}-logs.log', mode='a', maxBytes=100000, backupCount=5)
streamHandler = logging.StreamHandler()

handler.setFormatter(formatter)
rotatingHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

_logger.addHandler(handler)
_logger.addHandler(rotatingHandler)
_logger.addHandler(streamHandler)


def stopHandler(_signum, frame):
	onStop()


def onStop():
	global RUNNING
	RUNNING = False


def main():
	_logger.info('Starting Hermes Led Control version 3.0.4')

	signal.signal(signal.SIGINT, stopHandler)
	signal.signal(signal.SIGTERM, stopHandler)

	args = readConfiguration()

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
