# -*- coding: utf-8 -*-


import logging
import time
from multiprocessing import Process

import zmq
from matrix_io.proto.malos.v1 import driver_pb2
from matrix_io.proto.malos.v1 import io_pb2
from zmq.eventloop import ioloop, zmqstream


class Everloop:

	def __init__(self, numLeds, matrixIp, everloopPort):
		self._logger 		= logging.getLogger('SnipsLedControl')
		self._numLeds 		= numLeds
		self._matrixIp 		= matrixIp
		self._everloopPort 	= everloopPort
		self._driver 		= None

		self._context 		= zmq.Context()
		self._socket 		= self._context.socket(zmq.PUSH)

		self._colors 		= []

		ioloop.install()
		self._process = Process(target=self.register_error_callback, args=(self.everloopErrorCallback, self._matrixIp, self._everloopPort))
		self._process.daemon = True
		self._process.start()
		self.pingSocket()
		self.updateSocket()
		self.connectSocket()
		self.clear()


	def pingSocket(self):
		self._socket.connect('tcp://{0}:{1}'.format(self._matrixIp, self._everloopPort + 1))
		self._socket.send_string('')


	def updateSocket(self):
		context = zmq.Context()
		socket = context.socket(zmq.SUB)
		socket.connect('tcp://{0}:{1}'.format(self._matrixIp, self._everloopPort + 3))
		socket.setsockopt(zmq.SUBSCRIBE, b'')
		stream = zmqstream.ZMQStream(socket)
		stream.on_recv(self.updateLedCount)

		self._logger.info('Connected to data publisher with port {0}'.format(self._everloopPort + 3))
		ioloop.IOLoop.instance().start()


	def connectSocket(self):
		self._socket.connect('tcp://{0}:{1}'.format(self._matrixIp, self._everloopPort))


	def everloopErrorCallback(self, error):
		self._logger.error('{0}'.format(error))


	def updateLedCount(self, data):
		self._numLeds = io_pb2.LedValue().FromString(data[0]).green
		self._logger.info('Counted {} leds on device'.format(self._numLeds))
		if self._numLeds > 0:
			self._logger.info('LED count obtained. Disconnecting from data publisher {0}'.format(self._everloopPort + 3))
			ioloop.IOLoop.instance().stop()


	def setPixel(self, ledNum, red, green, blue, white):
		ledValue = io_pb2.LedValue()
		ledValue.red   = red
		ledValue.green = green
		ledValue.blue  = blue
		ledValue.white = white
		if ledNum < self._numLeds:
			self._colors[ledNum] = ledValue
		else:
			self._logger.warning("Led number missmatch ({}/{}), aborting".format(ledNum, self._numLeds))


	def _newArray(self):
		ledValue = io_pb2.LedValue()
		ledValue.blue  = 0
		ledValue.red   = 0
		ledValue.green = 0
		ledValue.white = 0
		self._colors = [ledValue] * self._numLeds


	def clear(self):
		self._newArray()
		self.show()


	def show(self):
		self._driver = driver_pb2.DriverConfig()
		self._driver.image.led.extend(self._colors)
		self._socket.send(self._driver.SerializeToString())


	def onStop(self):
		if self._process is not None:
			self._process.join(timeout=2)


	@staticmethod
	def register_data_callback(callback, creator_ip, sensor_port):
		"""Accepts a function to run when malOS zqm driver pushes an update"""

		# Grab a zmq context, as per usual, connect to it, but make it a SUBSCRIPTION this time
		context = zmq.Context()
		socket = context.socket(zmq.SUB)

		# Connect to the base sensor port provided in the args + 3 for the data port
		data_port = sensor_port + 3

		# Connect to the data socket
		socket.connect('tcp://{0}:{1}'.format(creator_ip, data_port))

		# Set socket options to subscribe and send off en empty string to let it know we're ready
		socket.setsockopt(zmq.SUBSCRIBE, b'')

		# Create the stream to listen to
		stream = zmqstream.ZMQStream(socket)

		# When data comes across the stream, execute the callback with it's contents as parameters
		stream.on_recv(callback)


	@staticmethod
	def register_error_callback(callback, creator_ip, sensor_port):
		"""Accepts a function to run when the malOS zqm driver pushes an error"""

		# Grab a zmq context, as per usual, connect to it, but make it a SUBSCRIPTION this time
		context = zmq.Context()
		socket = context.socket(zmq.SUB)

		# Connect to the base sensor port provided in the args + 2 for the error port
		error_port = sensor_port + 2

		# Connect to the data socket
		socket.connect('tcp://{0}:{1}'.format(creator_ip, error_port))

		# Set socket options to subscribe and send off en empty string to let it know we're ready
		socket.setsockopt(zmq.SUBSCRIBE, b'')

		# Create a stream to listen to
		stream = zmqstream.ZMQStream(socket)

		# When data comes across the stream, execute the callback with it's contents as parameters
		stream.on_recv(callback)

		# Start a global IO loop from tornado
		ioloop.IOLoop.instance().start()


	@staticmethod
	def driver_keep_alive(creator_ip, sensor_port, ping=5):
		"""
		This doesn't take a callback function as it's purpose is very specific.
		This will ping the driver every n seconds to keep the driver alive and sending updates
		"""

		# Grab zmq context
		context = zmq.Context()

		# Set up socket as a push
		sping = context.socket(zmq.PUSH)

		# Set the keep alive port to the sensor port from the function args + 1
		keep_alive_port = sensor_port + 1

		# Connect to the socket
		sping.connect('tcp://{0}:{1}'.format(creator_ip, keep_alive_port))

		# Start a forever loop
		while True:
			# Ping with empty string to let the drive know we're still listening
			sping.send_string('')

			# Delay between next ping
			time.sleep(ping)