#!/usr/bin/env python
# -*- coding: utf-8 -*-


from models.LedPattern import LedPattern
import time
import threading


class AlexaLedPattern(LedPattern):
	def __init__(self, controller):
		super(AlexaLedPattern, self).__init__(controller)
		self._animation 			= threading.Event()
		self._blank 				=[0, 0, 0]
		self._white 				= (255, 255, 255)
		self._blue 					= (0, 0, 255)
		self._defaultBrightness 	= 25


	@property
	def animation(self):
		return self._animation


	def wakeup(self, direction=0):
		for i in range(int(round(self._numLeds / 2)) + 1):
			self._controller.setLedRGB(i, self._white, 5 + (i * 2))
			self._controller.setLedRGB(self._numLeds - i, self._white, 5 + (i * 2))

			if i > 1:
				self._controller.setLedRGB(i - 2, self._blue, 5 + (i * 2))
				self._controller.setLedRGB(self._numLeds - i + 2, self._blue, 5 + (i * 2))

			self._controller.show()
			time.sleep(0.02)


	def listen(self):
		pass


	def think(self):
		first = self._blue
		second = self._white

		self._animation.set()
		while self._animation.isSet():
			for i in range(1, self._numLeds + 1):
				if not self._animation.isSet(): break

				if i % 2 == 0:
					self._controller.setLedRGB(i - 1, first, self._defaultBrightness)
				else:
					self._controller.setLedRGB(i - 1, second, self._defaultBrightness)

			self._controller.show()

			if first == self._blue:
				first = self._white
				second = self._blue
			else:
				first = self._blue
				second = self._white

			time.sleep(0.15)


	def speak(self):
		direction = 1
		red = 255
		green = 255

		for i in range(self._numLeds):
			self._controller.setLedRGB(i, self._white, self._defaultBrightness)

		self._animation.set()
		while self._animation.isSet():
			for i in range(self._numLeds):
				if not self._animation.isSet(): break
				self._controller.setLed(i, red=red, green=green, blue=255, brightness=self._defaultBrightness)
			self._controller.show()

			red -= direction
			green -= direction
			if red >= 255 or red <= 0:
				direction *= -1

			time.sleep(0.002)


	def off(self, *args):
		for i in range(int(round(self._numLeds / 2)) + 1):
			self._controller.setLedRGB(i, self._blank, 0)
			self._controller.setLedRGB(self._numLeds - i, self._blank, 0)

			self._controller.show()
			time.sleep(0.02)


	def idle(self, *args):
		self._controller.off()


	def onButton1(self, *args):
		# When mic mute button pressed
		for i in range(self._numLeds):
			self._controller.setLed(i, 60, 0, 0)
		self._controller.show()


	def onStart(self, *args):
		self._controller.wakeup()
		self._controller.off()
