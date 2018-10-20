#!/usr/bin/env python
# -*- coding: utf-8 -*-

class LedPattern:

	def __init__(self, numLeds, controller):
		self._numLeds 		= numLeds
		self._controller 	= controller


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


	def onError(self, *args):
		pass


	def onSuccess(self, *args):
		pass


	def off(self, *args):
		self._controller.clearLeds()


	def onStart(self, *args):
		pass


	def onStop(self, *args):
		self.off()