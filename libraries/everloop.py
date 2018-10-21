#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

class Everloop:

	def __init__(self, numLeds):
		self._numLeds 	= numLeds

		if not os.path.isfile('/dev/matrixio_everloop'):
			raise FileNotFoundError("Matrix Voice Everloop doesn't seem to be installed")

		self._colors = self._newArray()


	def setPixel(self, ledNum, red, green, blue, white):
		if ledNum <= 0 or ledNum > self._numLeds:
			raise IndexError('Trying to access a non existing led index')

		self._colors[ledNum - 1] = bytearray([red, green, blue, white])


	def _newArray(self):
		arr = []
		for i in range(0, self._numLeds):
			arr.append(bytearray([0, 0, 0, 0]))

		return arr


	def clear(self):
		self._newArray()
		self.show()


	def show(self):
		arr = bytearray()
		for ledColor in self._colors:
			arr += bytearray(ledColor)

		with open('/dev/matrixio_everloop', 'wb') as f:
			f.write(arr)
