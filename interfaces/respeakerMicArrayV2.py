#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.Exceptions 	import InterfaceInitError
from gpiozero 			import LED
from libraries 			import usb_pixel_ring_v2 	as pixel_ring
from models.Interface 	import Interface

class RespeakerMicArrayV2(Interface):

	def __init__(self, numLeds, vid, pid):
		super(RespeakerMicArrayV2, self).__init__(numLeds)

		#self._leds = pixel_ring.find(vid=hex(int(vid, 16)), pid=hex(int(pid, 16)))
		self._leds = pixel_ring.find()

		if self._leds is None:
			raise InterfaceInitError('Respeaker Mic Array V2 not found using pid={} and vid={}'.format(pid, vid))

		self._power 	= LED(5)
		self._colors 	= self._newArray()


	def setPixel(self, ledNum, red, green, blue, brightness):
		if ledNum < 0 or ledNum >= self._numLeds:
			self._logger.warning('Trying to access a led index out of reach')
			return

		index = ledNum * 4
		self._colors[index] = red
		self._colors[index + 1] = green
		self._colors[index + 2] = blue
		self._colors[index + 3] = brightness


	def setPixelRgb(self, ledNum, color, brightness):
		self.setPixel(ledNum, color[0], color[1], color[2], brightness)


	def clearStrip(self):
		self._colors = self._newArray()
		self.show()


	def show(self):
		self._leds.customize(self._colors)


	def _newArray(self):
		return [0, 0, 0, 0] * self._numLeds