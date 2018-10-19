#!/usr/bin/env python
# -*- coding: utf-8 -*-

from respeaker.apa102 import APA102
import time
import respeaker.pixels


class CustomLedPattern(object):
	def __init__(self, pixels, num_leds=3):

		self._leds 		= APA102(num_led=num_leds)
		self._pixels 	= pixels #type: respeaker.pixels.Pixels

		self._numLeds 	= num_leds
		self.stop 		= False


	def wakeup(self):
		self._leds.clear_strip()
		for brightness in range(101):
			for i in range(self._numLeds):
				self._leds.set_pixel(i, 0, 200, 0, brightness)

			self._leds.show()
			time.sleep(0.01)


	def listen(self):
		self._leds.clear_strip()
		direction = 1
		brightness = 0
		while not self.stop:
			for i in range(self._numLeds):
				self._leds.set_pixel(i, 0, 200, 0, brightness)

			self._leds.show()
			time.sleep(0.01)

			if brightness <= 0:
				direction = 1
			elif brightness >= 100:
				direction = -1

			brightness += direction

		for i in range(self._numLeds):
			self._leds.set_pixel(i, 0, 200, 0, 100)

		self._leds.clear_strip()


	def think(self):
		self._leds.clear_strip()
		while not self.stop:
			for i in range(self._numLeds):
				self._leds.set_pixel(i, 0, 200, 0, 100)
				time.sleep(0.2)

			self._leds.show()

			for i in reversed(range(self._numLeds)):
				self._leds.set_pixel(i, 0, 200, 0, 0)
				time.sleep(0.2)

		self._leds.clear_strip()


	def speak(self):
		self._leds.clear_strip()
		brightness = 100
		while not self.stop:
			for i in range(self._numLeds):
				self._leds.set_pixel(i, 0, 200, 0, brightness)
				time.sleep(0.05)

			if brightness == 100:
				brightness = 0
			else
				brightness = 100

			self._leds.show()

		self._leds.clear_strip()


	def idle(self):
		self._leds.clear_strip()
		direction = 1
		brightness = 0
		while not self.stop:
			for i in range(self._numLeds):
				self._leds.set_pixel(i, 0, 255, 0, brightness)

			self._leds.show()

			time.sleep(0.01)

			if brightness <= 0:
				direction = 1
			elif brightness >= 100:
				direction = -1

			brightness += direction

		self._leds.clear_strip()


	def off(self):
		self._leds.clear_strip()
