#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.Interface 	import Interface
from libraries.neopixel import *

try:
	import rpi_ws281x 	as ws
except ImportError:
	import _rpi_ws281x 	as ws

class Neopixels(Interface):

	def __init__(self, numLeds, pin):
		super(Neopixels, self).__init__(numLeds)

		self._pin 	= pin
		self._leds 	= Adafruit_NeoPixel(num=numLeds, pin=pin, brightness=100, strip_type=ws.SK6812_STRIP_RGBW)
		self._leds.begin()


	def setPixel(self, ledNum, red, green, blue, brightness):
		self._leds.setPixelColorRGB(ledNum, red, green, blue, brightness)


	def setPixelRgb(self, ledNum, color, brightness=None):
		self._leds.setPixelColor(ledNum, color)


	def clearStrip(self):
		for i in range(self._numLeds):
			self.setPixel(i, 0, 0, 0, 0)

		self.show()
