#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.LedPattern 			import LedPattern
import time
import threading


class CustomLedPattern(LedPattern):
	def __init__(self, controller):
		super(CustomLedPattern, self).__init__(self._controller)
		self._animation = threading.Event()


	@property
	def animation(self):
		return self._animation


	def wakeup(self, *args):
		for brightness in range(101):
			for i in range(self._numLeds):
				self._controller.setLed(i, 0, 200, 0, brightness)

			self._controller.show()
			time.sleep(0.01)


	def listen(self, *args):
		direction = 1
		brightness = 0

		self._animation.set()
		while self._animation.isSet():
			for i in range(self._numLeds):
				if not self._animation.isSet():
					break
				self._controller.setLed(i, 0, 200, 0, brightness)

			self._controller.show()
			time.sleep(0.01)

			if brightness <= 0:
				direction = 1
			elif brightness >= 100:
				direction = -1

			brightness += direction

		for i in range(self._numLeds):
			if not self._animation.isSet():
				break
			self._controller.setLed(i, 0, 200, 0, 100)


	def think(self, *args):
		self._animation.set()
		while self._animation.isSet():
			for i in range(self._numLeds):
				if not self._animation.isSet():
					break
				self._controller.setLed(i, 0, 200, 0, 100)
				time.sleep(0.2)

			self._controller.show()

			for i in reversed(range(self._numLeds)):
				if not self._animation.isSet():
					break
				self._controller.setLed(i, 0, 200, 0, 0)
				time.sleep(0.2)


	def speak(self, *args):
		brightness = 100

		self._animation.set()
		while self._animation.isSet():
			for i in range(self._numLeds):
				if not self._animation.isSet():
					break
				self._controller.setLed(i, 0, 20, 0, brightness)
				time.sleep(0.05)

			if brightness == 100:
				brightness = 0
			else:
				brightness = 100

			self._controller.show()


	def idle(self, *args):
		direction = 1
		brightness = 0

		self._animation.set()
		while self._animation.isSet():
			for i in range(self._numLeds):
				if not self._animation.isSet():
					break
				self._controller.setLed(i, 0, 0, 40, brightness)
			self._controller.show()

			time.sleep(0.01)

			if brightness <= 0:
				direction = 1
			elif brightness >= 100:
				direction = -1

			brightness += direction


	def onError(self, *args):
		for i in range(self._numLeds):
			self._controller.setLed(i, 125, 0, 0, 10)
		self._controller.show()
		time.sleep(0.7)


	def onSuccess(self, *args):
		for i in range(self._numLeds):
			self._controller.setLed(i, 0, 125, 0, 10)
		self._controller.show()
		time.sleep(0.7)


	def onStart(self, *args):
		self.wakeup()
		time.sleep(3)
		self.off()
	
	
	def onStop(self, *args):
		super(CustomLedPattern, self).onStop()