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
		for i in range(self._numLeds):
			self._image.append([0, 0, 0, 0])


	def rotate(self, color, speed, direction='cl', trail=0, startAt=0):
		"""
		Makes a light circulate your strip
		:param color: list, an array containing RGB or RGBW informations
		:param speed: float, in l/s or led per second
		:param direction: str, 'cl' or 'acl' defines the direction the light runs
		:param trail: int, if greater than 0, leave a trail behind the moving light, with decreased brightness
		:param startAt: int, the led index where the animation starts
		"""

		if trail > self._numLeds or trail < 0:
			self._logger.error("Trail can't be longer than amount of leds")
			return

		if startAt > self._numLeds - 1:
			self._logger.error("Cannot start at index {}, max index is {}".format(startAt, self._numLeds - 1))
			return

		self.new()

		# Create an image
		index = startAt
		self._setPixel(index, color)
		if trail > 0:
			fullBrightness = self._controller.defaultBrightness if len(color) < 4 else color[3]
			for i in range(1, trail + 1):
				if direction == 'cl':
					trailIndex = self._normalizeIndex(index - i)
				else:
					trailIndex = self._normalizeIndex(index + i)

				color[3] = int(fullBrightness / (i + 1))
				self._setPixel(trailIndex, color)

		self._displayImage()

		self._animationFlag.set()
		while self._animationFlag.isSet():
			time.sleep(1.0 / speed)
			if direction == 'cl':
				self._rotateImage(1)
			else:
				self._rotateImage(-1)
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


	def _rotateImage(self, step):
		if step == 0:
			self._logger.error('Cannot rotate by 0')
			return

		if step < 0:
			for i in range(0, step, -1):
				insertBack = self._image.pop(0)
				self._image.insert(len(self._image), insertBack)
		else:
			for i in range(step):
				insertBack = self._image.pop()
				self._image.insert(0, insertBack)


	def _normalizeIndex(self, index):
		"""
		Makes sure the given index is valid in the led strip or returns the one on the other side of the loop
		:param int index:
		:return: int
		"""
		if index < 0:
			return self._numLeds - abs(index)
		elif index >= self._numLeds:
			return index - self._numLeds
		else:
			return index