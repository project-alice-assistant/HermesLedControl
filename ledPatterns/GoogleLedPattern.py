#!/usr/bin/env python
# -*- coding: utf-8 -*-


from models.LedPattern import LedPattern
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


	def wakeup(self, direction=0):
		raise NotImplementedError()


	def listen(self):
		raise NotImplementedError()


	def think(self):
		raise NotImplementedError()


	def speak(self):
		raise NotImplementedError()



	def off(self):
		self._controller.showData([0] * 4 * self._numLeds)