#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libraries.everloop import Everloop
from models.Interface 	import Interface

class MatrixVoice(Interface):

	def __init__(self, numLeds):
		super(MatrixVoice, self).__init__(numLeds)

		try:
			self._leds = Everloop(numLeds)
		except FileNotFoundError:
			self._logger.error("Matrix Voice Everloop doesn't seem to be installed")
			raise KeyboardInterrupt


	def setPixel(self, ledNum, red, green, blue, brightness):
		self._leds.setPixel(ledNum=ledNum, red=red, green=green, blue=blue, white=brightness)


	def setPixelRgb(self, ledNum, color, brightness):
		self.setPixel(ledNum, color[0], color[1], color[2], brightness)


	def clearStrip(self):
		self._leds.clear()
