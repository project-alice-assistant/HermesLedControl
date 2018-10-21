#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libraries.everloop import Everloop
from models.Interface 	import Interface

class MatrixVoice(Interface):

	def __init__(self, numLeds):
		super(MatrixVoice, self).__init__(numLeds)
		self._leds 		= Everloop(numLeds)


	def setPixel(self, ledNum, red, green, blue, brightness):
		self._leds.setPixel(ledNum=ledNum, red=red, green=green, blue=blue, white=brightness)


	def setPixelRgb(self, ledNum, color, brightness):
		self._logger.warning('SetPixelRgb is not available for MatrixVoice interface')


	def clearStrip(self):
		self._leds.clear()
