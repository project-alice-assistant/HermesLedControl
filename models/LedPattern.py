#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from models.LedsController import *
import threading

class LedPattern(object):

	def __init__(self, controller):
		self._logger 		= logging.getLogger('SnipsLedControl')
		self._controller 	= controller # type: LedsController
		self._numLeds 		= self._controller.hardware['numberOfLeds']
		self._animation 	= threading.Event()


	@property
	def animation(self):
		return self._animation


	def wakeup(self, *args)		: pass
	def listen(self, *args)		: pass
	def think(self, *args)		: pass
	def speak(self, *args)		: pass
	def idle(self, *args)		: pass
	def off(self, *args)		: self._controller.clearLeds()
	def onError(self, *args)	: pass
	def onSuccess(self, *args)	: pass
	def onButton1(self, *args)	: self._logger.warning('Button 1 not implemented, override it in CustomLedPattern')
	def onButton2(self, *args)	: self._logger.warning('Button 2 not implemented, override it in CustomLedPattern')
	def onButton3(self, *args)	: self._logger.warning('Button 3 not implemented, override it in CustomLedPattern')
	def onButton4(self, *args)	: self._logger.warning('Button 4 not implemented, override it in CustomLedPattern')
	def onButton5(self, *args)	: self._logger.warning('Button 5 not implemented, override it in CustomLedPattern')
	def onButton6(self, *args)	: self._logger.warning('Button 6 not implemented, override it in CustomLedPattern')
	def onStart(self, *args)	: pass
	def onStop(self, *args)		: self.off()


	@staticmethod
	def color(red, green, blue, white=0):
		return (white << 24) | (red << 16) | (green << 8) | blue