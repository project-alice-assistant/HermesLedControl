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
		self._animation 		= threading.Event()

		self._cardinalSteps 	= int(math.ceil(self._numLeds / 4))
		self._colors 			= {
			'blue'		: [0, 0, 255, 15],
			'red'		: [255, 0, 0, 15],
			'yellow'	: [255, 255, 0, 15],
			'green'		: [0, 255, 0, 15]
		}


	@property
	def animation(self):
		return self._animation


	def rotate(self, direction, rounds):
		pass


	def wakeup(self):
		ledIndex = 0
		colors = list(self._colors)

		for i in range(4):
			self._controller.setLed(ledIndex, self._colors[colors[i - 1]][0], self._colors[colors[i - 1]][1], self._colors[colors[i - 1]][2], self._colors[colors[i - 1]][3])
			ledIndex += self._cardinalSteps
			if ledIndex >= self._numLeds:
				ledIndex -= self._numLeds

		self._controller.show()

		ledIndex = 7
		for i in range(self._numLeds * int(round(0.5))):
			self._controller.clearLeds()
			ledIndex += 1
			if ledIndex >= self._numLeds:
				ledIndex = 0

			pos = ledIndex
			for j in range(4):
				self._controller.setLed(pos, self._colors[colors[j - 1]][0], self._colors[colors[j - 1]][1], self._colors[colors[j - 1]][2], self._colors[colors[j - 1]][3])
				pos += self._cardinalSteps
				if pos >= self._numLeds:
					pos -= self._numLeds

			self._controller.show()
			time.sleep(0.025)


	def listen(self):
		self._controller.clearLeds()
		ledIndex = 0

		self._animation.set()
		while self._animation.isSet():
			self._controller.clearLeds()
			ledIndex += 1

			colors = list(self._colors)
			random.shuffle(colors)
			for i in range(4):
				self._controller.setLed(ledIndex, self._colors[colors[i - 1]][0], self._colors[colors[i - 1]][1], self._colors[colors[i - 1]][2], self._colors[colors[i - 1]][3])
				ledIndex += self._cardinalSteps
				if ledIndex >= self._numLeds:
					ledIndex -= self._numLeds

			self._controller.show()
			time.sleep(0.15)


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
				if ledIndex >= self._numLeds:
					ledIndex -= self._numLeds

			self._controller.show()
			time.sleep(0.03)


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

		self._controller.clearLeds()


	def off(self):
		self._controller.clearLeds()


	def onStart(self, *args):
		self.wakeup()
		self._controller.clearLeds()