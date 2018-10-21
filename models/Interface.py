#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

class Interface(object):

	def __init__(self, numLeds):
		self._numLeds 	= numLeds

		self._logger 	= logging.getLogger('SnipsLedControl')
		self._leds 		= None
		self._power 	= None


	@property
	def leds(self):
		return self._leds


	@property
	def numLeds(self):
		return self._numLeds


	def setPixel(self, ledNum, red, green, blue, brightness)	: pass
	def setPixelRgb(self, ledNum, color, brightness)			: pass
	def clearStrip(self)										: pass
	def show(self)												: self._leds.show()
	def onStart(self):
		if self._power is not None:
			self._power.on()
	def onStop(self):
		if self._power is not None:
			self._power.off()