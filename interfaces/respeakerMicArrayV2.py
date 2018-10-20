#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libraries import usb_pixel_ring_v2 as pixel_ring

class RespeakerMicArrayV2:

	def __init__(self, numLeds, vid, pid):
		self._numLeds 	= numLeds
		self._leds 		= pixel_ring.find(vid=vid, pid=pid)


	def set_pixel(self, ledNum, red, green, blue, brightness):
		self._leds.set_brightness = brightness
		self._leds.customize([red, green, blue, ledNum] * self._numLeds)


	def set_pixel_rgb(self, ledNum, rgb, brightness):
		pass


	def clear_strip(self):
		self._leds.write(6)


	def show(self):
		self._leds.show()