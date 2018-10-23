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
			'blue': [0, 0, 255, 15],
			'red': [255, 0, 0, 15],
			'yellow': [255, 255, 0, 15],
			'green': [0, 255, 0, 15]
		}


	@property
	def animation(self):
		return self._animation


	def wakeup(self, direction=0):
		step = int(math.ceil(self._numLeds / 4))

		ledIndex = 0
		colors = list(self._colors)
		for i in range(4):
			if not self._animation.isSet():
				break

			self._controller.setLed(ledIndex, self._colors[colors[i - 1]][0], self._colors[colors[i - 1]][1], self._colors[colors[i - 1]][2], self._colors[colors[i - 1]][3])
			self._controller.show()
			ledIndex += step
			time.sleep(0.1)


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
				self._controller.setLed(ledIndex, self._colors[colors[i - 1]][0], self._colors[colors[i - 1]][1], self._colors[colors[i - 1]][2], self._colors[colors[i - 1]][3])
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
				self._controller.setLed(ledIndex, self._colors[colors[i - 1]][0], self._colors[colors[i - 1]][1], self._colors[colors[i - 1]][2], self._colors[colors[i - 1]][3])
				ledIndex += step
				if ledIndex >= 12:
					ledIndex -= 12

			self._controller.show()
			time.sleep(0.1)


	def speak(self):
		self._controller.clearLeds()
		step = int(math.ceil(self._numLeds / 4))
		colors = list(self._colors)
		direction = 1
		bright = -20

		self._animation.set()
		while self._animation.isSet():
			direction *= -1
			bright *= direction
			for i in range(bright):
				ledIndex = 0
				for j in range(4):
					self._controller.setLed(ledIndex, self._colors[colors[j - 1]][0], self._colors[colors[j - 1]][1], self._colors[colors[j - 1]][2], self._colors[colors[j - 1]][3] + i * direction)
					ledIndex += step

				self._controller.show()
				time.sleep(0.025)


	def off(self):
		self._controller.clearLeds()


	def onStart(self, *args):
		self.wakeup()
		time.sleep(1)
		self._controller.clearLeds()