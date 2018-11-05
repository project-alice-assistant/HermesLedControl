#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import zmq
import time
from random import randint
from matrix_io.proto.malos.v1 import driver_pb2
from matrix_io.proto.malos.v1 import io_pb2
from multiprocessing import Process
from zmq.eventloop import ioloop, zmqstream
from utils import register_error_callback

class Everloop:

	def __init__(self, numLeds, matrixIp, everloopPort):
		self._logger 		= logging.getLogger('SnipsLedControl')
		self._numLeds 		= numLeds
		self._matrixIp 		= matrixIp
		self._everloopPort 	= everloopPort

		self._driver 		= driver_pb2.DriverConfig()
		self._context 		= zmq.Context()
		self._socket 		= self._context.socket(zmq.PUSH)

		self._colors 		= self._newArray()

		ioloop.install()
		Process(target=register_error_callback, args=(self.everloopErrorCallback, self._matrixIp, self._everloopPort)).start()
		self.pingSocket()
		self.updateSocket()
		self.configSocket(self._numLeds)


	def pingSocket(self):
		self._socket.connect('tcp://{0}:{1}'.format(self._matrixIp, self._everloopPort + 1))
		self._socket.send_string('')


	def updateSocket(self):
		socket = self._context.socket(zmq.SUB)
		socket.connect('tcp://{0}:{1}'.format(self._matrixIp, self._everloopPort + 3))
		socket.setsockopt(zmq.SUBSCRIBE, b'')
		stream = zmqstream.ZMQStream(socket)
		stream.on_recv(self.updateLedCount)

		self._logger.info('Connected to data publisher with port {0}'.format(self._everloopPort + 3))
		ioloop.IOLoop.instance().start()


	def configSocket(self, ledCount):
		self._socket.connect('tcp://{0}:{1}'.format(self._matrixIp, self._everloopPort))

		while True:
			image = []
			# For each device LED
			for led in range(ledCount):
				# Set individual LED value
				ledValue = io_pb2.LedValue()
				ledValue.blue = randint(0, 50)
				ledValue.red = randint(0, 200)
				ledValue.green = randint(0, 255)
				ledValue.white = 0
				image.append(ledValue)

			self._driver.image.led.extend(image)

			self._socket.send(self._driver.SerializeToString())
			time.sleep(0.05)


	def everloopErrorCallback(self, error):
		self._logger.error('{0'.format(error))


	def updateLedCount(self, data):
		self._numLeds = io_pb2.LedValue().FromString(data[0]).green
		self._logger.info('{0} LEDs counted'.format(self._numLeds))
		if self._numLeds > 0:
			self._logger.info('LED count obtained. Disconnecting from data publisher {0}'.format(self._everloopPort + 3))
			ioloop.IOLoop.instance().stop()


	def setPixel(self, ledNum, red, green, blue, white):
		ledValue = io_pb2.LedValue()
		ledValue.red = red
		ledValue.green = green
		ledValue.blue = blue
		ledValue.white = white
		self._colors[ledNum] = ledValue


	def _newArray(self):
		ledValue = io_pb2.LedValue()
		return [ledValue] * self._numLeds


	def clear(self):
		self._newArray()
		self.show()


	def show(self):
		self._driver.image.led.extend(self._colors)
		self._socket.send(self._driver.SerializeToString())
