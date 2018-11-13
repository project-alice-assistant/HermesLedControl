#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time

class Animations:
	def __init__(self, animationFlag, controller):
		self._logger 		= logging.getLogger('SnipsLedControl')
		self._animationFlag = animationFlag
		self._controller 	= controller
		self._numLeds 		= self._controller.hardware['numberOfLeds']
		self._image 		= []
		self.new()


	def new(self):
		self._image = []
		for i in self._numLeds:
			self._image.append([0, 0, 0, 0])


	def rotate(self, color, direction, speed, trail, startAt=0):
		"""
		Makes a light circulate your strip
		:param color: list, an array containing RGB or RGBW informations
		:param direction: str, 'cl' or 'acl' defines the direction the light runs
		:param speed: float, in l/s or led per second
		:param trail: int, if greater than 0, leave a trail behind the moving light, with decreased brightness
		:param startAt: int, the led index where the animation starts
		"""

		if trail > self._numLeds:
			self._logger.error("Trail can't be longer than amount of leds")
			return

		self.new()

		index = startAt
		self._setPixel(index, color)
		self._animationFlag.set()
		while self._animationFlag.isSet():
			time.sleep(speed)
			self._setPixel(index, [0, 0, 0, 0])

			if direction == 'cl':
				index = index + 1
			else:
				index = index - 1

			if index < 0:
				index = self._numLeds - 1
			elif index >= self._numLeds:
				index = 0

			self._setPixel(index, color)
			self._displayImage()


	def _setPixel(self, index, color):
		if index >= len(self._image):
			self._logger.error("Cannot assign led index {}, out of bound".format(index))
			return

		self._image[index] = color


	def _displayImage(self):
		for i, led in enumerate(self._image):
			self._controller.setLedRGB(i, led)

		self._controller.show()