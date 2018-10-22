#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gpiozero 			import LED
from libraries 			import usb_pixel_ring_v2 	as pixel_ring
from models.Interface 	import Interface

class RespeakerMicArrayV2(Interface):

	def __init__(self, numLeds, vid, pid):
		super(RespeakerMicArrayV2, self).__init__(numLeds)

		self._leds 		= pixel_ring.find(vid=vid, pid=pid)
		if self._leds is None:
			self._logger.critical('Respeaker Mic Array V2 not found using pid={} and vid={}'.format(pid, vid))
			return

		self._power 	= LED(5)
		self._colors 	= self._newArray()


	def setPixel(self, ledNum, red, green, blue, brightness):
		self._leds.set_brightness = brightness
		self._leds.customize([red, green, blue, ledNum] * self._numLeds)


	def setPixelRgb(self, ledNum, color, brightness):
		self._logger.warning('SetPixelRgb is not available for RespeakerMicArrayV2 interface')
		pass


	def clearStrip(self):
		self._leds.write(6)


	def show(self):
		arr = bytearray()
		for ledColor in self._colors:
			arr += bytearray(ledColor)

		self._leds.show(arr)


	def _newArray(self):
		arr = []
		for i in range(0, self._numLeds):
			arr.append([0, 0, 0, 0])

		return arr