#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.LedPattern import LedPattern
import time
import threading


class CustomLedPattern(LedPattern):

	def __init__(self, controller):
		super(CustomLedPattern, self).__init__(controller)
		self._animation = threading.Event()


	@property
	def animation(self):
		return self._animation


	def breathLeds(self, duration=1.0, color=None, leds=None):  # smootly light up and down, all or specified leds by numbers
		if leds is None:
			leds = []
		if color is None:
			color = [0, 0, 40]

		if len(leds) == 0:
			leds = [i for i in range(self._numLeds)]

		pause = float(duration / 200.00)
		direction = 1
		brightness = 0

		frame = 0
		while frame < duration:
			for l in leds:
				self._controller.setLed(l, color[0], color[1], color[2], brightness)

			self._controller.show()

			time.sleep(pause)

			if brightness <= 0:
				direction = 1
			elif brightness >= 100:
				direction = -1

			brightness += direction
			frame += pause


	def tailTranslate(self, duration=0.5, color=None, invert=False):  # progressive translation of all leds
		if color is None:
			color = [0, 0, 40, 0]

		pause = float(duration / (self._numLeds * 2))
		step = int(100 / self._numLeds + 1)

		for i in range(self._numLeds):
			self._controller.setLed(i, color[0], color[1], color[2], 0)
			self._controller.show()

		refs = [0 for i in range(self._numLeds)]
		refs[0] = 100

		for i in range(self._numLeds):
			for j in range(i, 0, -1):
				if refs[j] >= step:
					refs[j - 1] = refs[j] - step
				else:
					refs[j - 1] = 0

			if invert: refs = list(reversed(refs))

			for l in range(self._numLeds):
				self._controller.setLed(l, color[0], color[1], color[2], refs[l])
				self._controller.show()

			if invert: refs = list(reversed(refs))

			time.sleep(pause)
			refs.pop()
			refs.insert(0, 0)

		for i in range(self._numLeds):
			if invert: refs = list(reversed(refs))
			for l in range(self._numLeds):
				self._controller.setLed(l, color[0], color[1], color[2], refs[l])
				self._controller.show()
			if invert: refs = list(reversed(refs))
			refs.pop()
			refs.insert(0, 0)
			time.sleep(pause)


	def translate(self, duration=0.5, color=None, leds=None, invert=False):  # translation of specified leds
		if leds is None:
			leds = []
		if color is None:
			color = [0, 0, 40, 0]

		if len(leds) == 0:
			leds = [int(self._numLeds / 2)]

		pause = float(duration / (self._numLeds + 1))
		refs = [0 for i in range(self._numLeds)]

		for i in range(self._numLeds):
			if i in leds:
				refs[i] = 100

		for i in range(self._numLeds + 1):
			if invert: refs = list(reversed(refs))
			for l in range(self._numLeds):
				self._controller.setLed(l, color[0], color[1], color[2], refs[l])
				self._controller.show()
			if invert: refs = list(reversed(refs))
			time.sleep(pause)
			refs.pop()
			refs.insert(0, 0)


	def wakeup(self, *args):
		self._controller.clearLeds()
		self.tailTranslate(0.5, [100, 0, 0])
		self.tailTranslate(0.5, [100, 0, 0], True)


	def listen(self, *args):
		self._controller.clearLeds()
		self._animation.set()
		while self._animation.isSet():
			self.breathLeds(0.5, [0, 0, 90])


	def think(self, *args):
		self._controller.clearLeds()
		self._animation.set()
		while self._animation.isSet():
			self.tailTranslate(0.5, [180, 140, 60])
			self.tailTranslate(0.5, [180, 140, 60], True)


	def speak(self, *args):
		self._controller.clearLeds()
		leds = [i for i in range(self._numLeds)]
		del leds[int(self._numLeds / 2)]
		self._animation.set()
		while self._animation.isSet():
			self.breathLeds(0.5, [0, 0, 90], leds)


	def idle(self, *args):
		self._controller.clearLeds()
		self._animation.set()
		while self._animation.isSet():
			self.breathLeds(1, [0, 0, 60])


	def onError(self, *args):
		self._controller.clearLeds()
		for i in range(self._numLeds):
			self._controller.setLed(i, 120, 0, 0, 100)
		self._controller.show()
		time.sleep(0.7)


	def onSuccess(self, *args):
		for i in range(self._numLeds):
			self._controller.setLed(i, 0, 120, 0, 100)
		self._controller.show()
		time.sleep(0.7)


	def onStart(self, *args):
		self.wakeup()