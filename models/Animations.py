# -*- coding: utf-8 -*-

import logging
import math
import time

class Animations:
	def __init__(self, animationFlag, controller):
		self._logger 		= logging.getLogger('SnipsLedControl')
		self._animationFlag = animationFlag
		self._controller 	= controller
		self._numLeds 		= self._controller.hardware['numberOfLeds']
		self._image 		= []
		self.new()


	def new(self, image=None):
		self._controller.clearLeds()
		if image is not None:
			self._image = image
		else:
			self._image = []
			for i in range(self._numLeds):
				self._image.append([0, 0, 0, 0])


	def rotateImage(self, step):
		"""
		Rotates an image by step number of led
		:param step: int Positive for clockwise, negative for anti clockwise
		"""
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
		self._displayImage()


	def rotate(self, color, speed=10, trail=0, startAt=0):
		"""
		Makes a light circulate your strip
		:param color: list, an array containing RGB or RGBW informations
		:param speed: float, in l/s or led per second
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
				if speed >= 0:
					trailIndex = self._normalizeIndex(index - i)
				else:
					trailIndex = self._normalizeIndex(index + i)

				color[3] = int(math.ceil(float(fullBrightness / (i + 1))))
				self._setPixel(trailIndex, color)

		self._displayImage()

		self._animationFlag.set()
		while self._animationFlag.isSet():
			time.sleep(1.0 / abs(speed))
			if speed >= 0:
				self.rotateImage(1)
			else:
				self.rotateImage(-1)


	def relayRace(self, color, relayColor, backgroundColor=None, speed=10, startAt=0):
		"""
		:param color: array RGBW
		:param relayColor: array RGBW
		:param backgroundColor: array RGBW
		:param speed: float, in l/s or led per second
		:param startAt: int, the led index where the animation starts
		"""
		if backgroundColor is None:
			backgroundColor = [0, 0, 0, 0]

		self.new()
		for i in range(self._numLeds):
			self._setPixel(i, backgroundColor)

		index = startAt
		self._animationFlag.set()
		while self._animationFlag.isSet():
			self._setPixel(index, color)
			if speed >= 0:
				relayIndex = self._normalizeIndex(index + 1)
			else:
				relayIndex = self._normalizeIndex(index - 1)

			self._setPixel(relayIndex, relayColor)
			self._displayImage()
			while self._animationFlag.isSet() and relayIndex != index:
				time.sleep(1.0 / abs(speed))
				self._setPixel(relayIndex, backgroundColor)

				if speed >= 0:
					relayIndex = self._normalizeIndex(relayIndex + 1)
				else:
					relayIndex = self._normalizeIndex(relayIndex - 1)

				self._setPixel(relayIndex, relayColor)
				self._displayImage()

			self._setPixel(index, backgroundColor)
			if speed >= 0:
				index = self._normalizeIndex(index + 1)
			else:
				index = self._normalizeIndex(index - 1)


	def doublePingPong(self, color, speed=10, backgroundColor=None, startAt=0):
		"""
		Makes two balls ping pong
		:param color: array RBGW
		:param speed: float, in l/s or led per second
		:param backgroundColor: array RGBW
		:param startAt: int, the led index where the animation starts
		:return:
		"""
		if backgroundColor is None:
			backgroundColor = [0, 0, 0, 0]

		self.new()
		self._setPixel(startAt, color)

		index = startAt
		self._animationFlag.set()
		while self._animationFlag.isSet():
			self._displayImage()
			self._setPixel(startAt, [0, 0, 0, 0])
			step = 0
			while self._animationFlag.isSet() and step != self._numLeds / 2:
				step += 1
				leftIndex = self._normalizeIndex(index - step)
				rightIndex = self._normalizeIndex(index + step)
				self._setPixel(leftIndex, color)
				self._setPixel(rightIndex, color)
				self._displayImage()
				time.sleep(1.0 / abs(speed))
				self._setPixel(leftIndex, [0, 0, 0, 0])
				self._setPixel(rightIndex, [0, 0, 0, 0])
			while self._animationFlag.isSet() and step >= 0:
				step -= 1
				leftIndex = self._normalizeIndex(index + step)
				rightIndex = self._normalizeIndex(index - step)
				self._setPixel(leftIndex, color)
				self._setPixel(rightIndex, color)
				self._displayImage()
				time.sleep(1.0 / abs(speed))
				self._setPixel(leftIndex, [0, 0, 0, 0])
				self._setPixel(rightIndex, [0, 0, 0, 0])


	def waitWheel(self, color, speed=10, backgroundColor=None, startAt=0):
		"""
		Makes two balls ping pong
		:param color: array RBGW
		:param speed: float, in l/s or led per second
		:param backgroundColor: array RGBW
		:param startAt: int, the led index where the animation starts
		:return:
		"""
		if backgroundColor is None:
			backgroundColor = [0, 0, 0, 0]

		self.new()
		self._setPixel(startAt, color)

		index = startAt
		self._animationFlag.set()
		while self._animationFlag.isSet():
			time.sleep(1.0 / abs(speed))
			self._displayImage()
			index += 1
			index = self._normalizeIndex(index)

			if self._image[index] == color:
				self._setPixel(index, backgroundColor)
			else:
				self._setPixel(index, color)

	def _setPixel(self, index, color):
		if index >= len(self._image) or index < 0:
			self._logger.error("Cannot assign led index {}, out of bound".format(index))
			return
		self._image[index] = [color[0], color[1], color[2], color[3]]


	def _displayImage(self):
		for i, led in enumerate(self._image):
			self._controller.setLedRGB(i, led)

		self._controller.show()


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