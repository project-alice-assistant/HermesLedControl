# -*- coding: utf-8 -*-

from libraries.everloop import Everloop
from models.Exceptions import InterfaceInitError
from models.Interface import Interface


class MatrixVoice(Interface):

	def __init__(self, numLeds, matrixIp, everloopPort):
		super(MatrixVoice, self).__init__(numLeds)

		try:
			self._leds = Everloop(numLeds, matrixIp, everloopPort)
		except:
			raise InterfaceInitError("Couldn't initialize everloop")


	def setPixel(self, ledNum, red, green, blue, brightness):
		self._leds.setPixel(ledNum=ledNum, red=red, green=green, blue=blue, white=brightness)


	def setPixelRgb(self, ledNum, color, brightness):
		self.setPixel(ledNum, color[0], color[1], color[2], brightness)


	def clearStrip(self):
		self._leds.clear()


	def onStop(self):
		self.clearStrip()
		self._leds.onStop()
		super(MatrixVoice, self).onStop()