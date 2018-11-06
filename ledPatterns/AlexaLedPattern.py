#!/usr/bin/env python
# -*- coding: utf-8 -*-


from models.LedPattern import LedPattern
import time
import threading


class AlexaLedPattern(LedPattern):
	def __init__(self, controller):
		super(AlexaLedPattern, self).__init__(controller)
		self._animation = threading.Event()


	@property
	def animation(self):
		return self._animation


	def wakeup(self, direction=0):
		for i in range(int(round(self._numLeds / 2)) + 1):
			self._controller.setLed(i, 255, 255, 255, 5 + (i * 2))
			self._controller.setLed(self._numLeds - i, 255, 255, 255, 5 + (i * 2))

			if i > 1:
				self._controller.setLed(i - 2, 0, 0, 255, 5 + (i * 2))
				self._controller.setLed(self._numLeds - i + 2, 0, 0, 255, 5 + (i * 2))

			self._controller.show()
			time.sleep(0.02)


	def listen(self):
		pass


	def think(self):
		for i in range(self._numLeds):
			self._controller.setLed(i, 255, 255, 255, 50)
		self._controller.show()


	def speak(self):
		raise NotImplementedError()


	def onButton1(self, *args):
		# When mic mute button pressed
		for i in range(self._numLeds):
			self._controller.setLed(i, 60, 0, 0)
		self._controller.show()


	def onStart(self, *args):
		self._controller.wakeup()