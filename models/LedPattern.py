#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.LedsController import *

class LedPattern:

	def __init__(self, controller):
		self._controller: LedsController = controller
		self._numLeds = self._controller.hardware['numberOfLeds']


	def wakeup(self, *args):
		pass


	def listen(self, *args):
		pass


	def think(self, *args):
		pass


	def speak(self, *args):
		pass


	def idle(self, *args):
		pass


	def off(self, *args):
		self._controller.clearLeds()


	def onError(self, *args):
		pass


	def onSuccess(self, *args):
		pass

	def onStart(self, *args):
		pass


	def onStop(self, *args):
		self.off()