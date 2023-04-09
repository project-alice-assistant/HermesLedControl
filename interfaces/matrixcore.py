from models.Interface import Interface

import zmq
from matrix_io.proto.malos.v1 import driver_pb2 # MATRIX Protocol Buffer driver library
from matrix_io.proto.malos.v1 import io_pb2 # MATRIX Protocol Buffer sensor library

import asyncio
import zmq.asyncio

from typing import Any, Awaitable

class MatrixCore(Interface):

	def __init__(self, matrixIp: str, everloopPort: int, numLeds: int):
		super(MatrixCore, self).__init__(numLeds)

		self._matrixIp: str = matrixIp
		self._everloopPort: int = everloopPort

		self.context: zmq.asyncio.Context = zmq.asyncio.Context()

		matrixNumLeds: int = asyncio.run(self._initMatrixConnection())
		self._logger.info('Sucessfully connected - matrix has %i LEDs', matrixNumLeds)

		self._actualNumLeds = numLeds
		if numLeds > matrixNumLeds:
			self._logger.warn('The configured hardware is supposed to have %i LEDs but only has %i.', numLeds, matrixNumLeds)
			self._actualNumLeds = matrixNumLeds
		
		self._image = self._newArray()

		self._everloopSocket = self.context.socket(zmq.PUSH)
		self._everloopSocket.connect('tcp://{0}:{1}'.format(self._matrixIp, self._everloopPort))

	def setPixel(self, ledNum, red, green, blue, brightness):
		if ledNum < 0 or ledNum >= self._actualNumLeds:
			self._logger.warning('Trying to access a led index out of reach (%i)', ledNum)
			return

		color = self._image[ledNum]
		color.red = red
		color.green = green
		color.blue = blue
		color.white = brightness


	def setPixelRgb(self, ledNum, color, brightness):
		self.setPixel(ledNum, color[0], color[1], color[2], brightness)


	def clearStrip(self):
		self._image = self._newArray()
		self.show()


	def show(self):
		asyncio.run(self._show())

	async def _show(self) -> Awaitable[None]:
		driver_config_proto = driver_pb2.DriverConfig()
		driver_config_proto.image.led.extend(self._image)
		await self._everloopSocket.send(driver_config_proto.SerializeToString())

	async def _initMatrixConnection(self) -> Awaitable[int]:
		self._logger.info('Connecting to matrix everloop %s:%i', self._matrixIp, self._everloopPort)

		updateSocket = self.context.socket(zmq.SUB)
		updateSocket.connect('tcp://{0}:{1}'.format(self._matrixIp, self._everloopPort+3))
		updateSocket.setsockopt(zmq.SUBSCRIBE, b'')
		update = updateSocket.recv()

		pingSocket = self.context.socket(zmq.PUSH)
		pingSocket.connect('tcp://{0}:{1}'.format(self._matrixIp, self._everloopPort+1))
		
		try:
			pingSocket.send_string('')
			data: Any = await update
			return io_pb2.LedValue().FromString(data).green
		except Exception as e:
			self._logger.exception(e)
		finally:
			pingSocket.close()
			updateSocket.close()
		
		return 18
	
	def onStop(self):
		self._everloopSocket.close()

	def _newArray(self):
		return [io_pb2.LedValue() for _ in range(self._actualNumLeds)]
