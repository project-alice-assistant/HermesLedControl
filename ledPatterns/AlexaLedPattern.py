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
import time
import threading


class AlexaLedPattern(LedPattern):
	def __init__(self, controller):
		super(AlexaLedPattern, self).__init__(controller)
		self.pixels = [0] * 4 * self._numLeds

		self._animation = threading.Event()

	def wakeup(self, direction=0):
		position = int((direction + 15) / (360 / self._numLeds)) % self._numLeds

		pixels = [0, 0, 0, 24] * self._numLeds
		pixels[position * 4 + 2] = 48

		self._controller.showData(pixels)

	def listen(self):
		pixels = [0, 0, 0, 24] * self._numLeds

		self._controller.showData(pixels)

	def think(self):
		pixels  = [0, 0, 12, 12, 0, 0, 0, 24] * self._numLeds

		self._animation.set()
		while self._animation.isSet():
			self._controller.showData(pixels)
			time.sleep(0.2)
			pixels = pixels[-4:] + pixels[:-4]

	def speak(self):
		step = 1
		position = 12
		self._animation.set()
		while self._animation.isSet():
			pixels  = [0, 0, position, 24 - position] * self._numLeds
			self._controller.showData(pixels)
			time.sleep(0.01)
			if position <= 0:
				step = 1
				time.sleep(0.4)
			elif position >= 12:
				step = -1
				time.sleep(0.4)

			position += step

	def idle(self):
		self._controller.showData([0] * 4 * 12)

	def onError(self):
		self._controller.showData([0] * 4 * 12)

	def onSuccess(self):
		self._controller.showData([0] * 4 * 12)

	def off(self):
		self._controller.showData([0] * 4 * 12)
