#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Seeed Technology Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from models.LedPattern import LedPattern
import numpy
import time
import threading
try:
	import queue as Queue
except ImportError:
	import Queue as Queue


class GoogleHomeLedPattern(LedPattern):
	def __init__(self, controller):
		super(GoogleHomeLedPattern, self).__init__(controller)
		self.basis = numpy.array([0] * 4 * 12)
		self.basis[0 * 4 + 1] = 2
		self.basis[3 * 4 + 1] = 1
		self.basis[3 * 4 + 2] = 1
		self.basis[6 * 4 + 2] = 2
		self.basis[9 * 4 + 3] = 2

		self.pixels = self.basis * 24
		self._animation = threading.Event()

	def wakeup(self, direction=0):
		position = int((direction + 15) / 30) % 12

		basis = numpy.roll(self.basis, position * 4)
		for i in range(1, 25):
			pixels = basis * i
			self._controller.showData(pixels)
			time.sleep(0.005)

		pixels =  numpy.roll(pixels, 4)
		self._controller.showData(pixels)
		time.sleep(0.1)

		for i in range(2):
			new_pixels = numpy.roll(pixels, 4)
			self._controller.showData(new_pixels * 0.5 + pixels)
			pixels = new_pixels
			time.sleep(0.1)

		self._controller.showData(pixels)
		self.pixels = pixels

	def listen(self):
		pixels = self.pixels
		for i in range(1, 25):
			self._controller.showData(pixels * i / 24)
			time.sleep(0.01)

	def think(self):
		pixels = self.pixels

		self._animation.set()
		while self._animation.isSet():
			pixels = numpy.roll(pixels, 4)
			self._controller.showData(pixels)
			time.sleep(0.2)

		t = 0.1
		for i in range(0, 5):
			pixels = numpy.roll(pixels, 4)
			self._controller.showData(pixels * (4 - i) / 4)
			time.sleep(t)
			t /= 2

		self.pixels = pixels

	def speak(self):
		pixels = self.pixels
		step = 1
		brightness = 5
		self._animation.set()
		while self._animation.isSet():
			self._controller.showData(pixels * brightness / 24)
			time.sleep(0.02)

			if brightness <= 5:
				step = 1
				time.sleep(0.4)
			elif brightness >= 24:
				step = -1
				time.sleep(0.4)

			brightness += step

	def idle(self):
		self._controller.showData([0] * 4 * 12)

	def onError(self):
		self._controller.showData([0] * 4 * 12)

	def onSuccess(self):
		self._controller.showData([0] * 4 * 12)

	def off(self):
		self._controller.showData([0] * 4 * 12)


