#!/usr/bin/env python
# -*- coding: utf-8 -*-

from neopixel import *

try:
	import rpi_ws281x as ws
except ImportError:
	import _rpi_ws281x as ws

class Neopixels:

	def __init__(self, numLeds, pin):
		self._numLeds 	= numLeds
		self._pin 		= pin
		self._leds 		= Adafruit_NeoPixel(num=numLeds, pin=pin, brightness=100, strip_type=ws.SK6812_STRIP_RGBW)
		self._leds.begin()


	def set_pixel(self, ledNum, red, green, blue, brightness):
		self._leds.setBrightness = brightness
		self._leds.setPixelColor(ledNum, green, red, blue)


	def set_pixel_rgb(self, ledNum, rgb, brightness):
		self._leds.setBrightness = brightness
		self._leds.setPixelColorRGB(ledNum, rgb)


	def clear_strip(self):
		for i in range(self._numLeds):
			self.set_pixel(i, 0, 0, 0, 0)

		self.show()


	def show(self):
		self._leds.show()