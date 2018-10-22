#!/usr/bin/env python
# -*- coding: utf-8 -*-


from models.LedPattern import LedPattern
import math
import random
import time
import threading
try:
	import queue as Queue
except ImportError:
	import Queue as Queue

class GoogleHomeLedPattern(LedPattern):

	def __init__(self, controller):
		super(GoogleHomeLedPattern, self).__init__(controller)
		self._animation = threading.Event()

		self._colors = {
			'blue': [23, 107, 239],
			'red': [255, 62, 48],
			'yellow': [247, 181, 41],
			'green': [23, 156, 82]
		}


	@property
	def animation(self):
		return self._animation


	def wakeup(self, direction=0):
		step = int(math.ceil(self._numLeds / 4))

		ledIndex = 0
		colors = list(self._colors)
		for i in range(4):
			self._controller.setLed(ledIndex, self._colors[colors[i - 1]][0], self._colors[colors[i - 1]][1], self._colors[colors[i - 1]][2], 100)
			ledIndex += step

		self._controller.show()


	def listen(self):
		step = int(math.ceil(self._numLeds / 4))
		ledIndex = 0

		self._animation.set()
		while self._animation.isSet():
			self._controller.clearLeds()
			ledIndex += 1

			colors = list(self._colors)
			random.shuffle(colors)
			for i in range(4):
				self._controller.setLed(ledIndex, self._colors[colors[i - 1]][0], self._colors[colors[i - 1]][1], self._colors[colors[i - 1]][2], 100)
				ledIndex += step
				if ledIndex >= 12:
					ledIndex -= 12

			self._controller.show()
			time.sleep(0.3)


	def think(self):
		step = int(math.ceil(self._numLeds / 4))
		ledIndex = 0

		self._animation.set()
		while self._animation.isSet():
			self._controller.clearLeds()
			ledIndex += 1

			colors = list(self._colors)
			for i in range(4):
				self._controller.setLed(ledIndex, self._colors[colors[i - 1]][0], self._colors[colors[i - 1]][1], self._colors[colors[i - 1]][2], 100)
				ledIndex += step
				if ledIndex >= 12:
					ledIndex -= 12

			self._controller.show()
			time.sleep(0.01)


	def speak(self):
		raise NotImplementedError()


	def off(self):
		self._controller.clearLeds()