#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################################################################
# SUBMIT YOUR OWN CUSTOM PATTERN AND SHARE WITH THE WORLD YOUR LED ANIMATIONS!
# Visit https://github.com/Psychokiller1888/snipsLedControl/issues/new?template=custom-pattern-proposal.md
# for more informations
#
# Check models/LedPattern.py for the available functions
# Do NEVER have a function call a super class function directly!!
# It could cause a deadlock! Instead, call self._controller.THE_METHOD_YOU_WANT
###########################################################################################################

from models.LedPattern import LedPattern
import time

class CustomLedPattern(LedPattern):

	def __init__(self, controller):
		super(CustomLedPattern, self).__init__(controller)


	def think(self, *args):
		# image = [
		# 	[0, 0, 125, 100],
		# 	[0, 0, 0, 0],
		# 	[0, 0, 0, 0],
		# 	[0, 125, 0, 100],
		# 	[0, 0, 0, 0],
		# 	[0, 0, 0, 0],
		# 	[125, 0, 0, 100],
		# 	[0, 0, 0, 0],
		# 	[0, 0, 0, 0],
		# 	[125, 0, 125, 100],
		# 	[0, 0, 0, 0],
		# 	[0, 0, 0, 0]
		# ]
		# self._animationTemplate.new(image=image)
		#
		# for i in range(36):
		# 	self._animationTemplate.rotateImage(1)
		# 	time.sleep(0.1)
		#
		# for i in range(72):
		# 	self._animationTemplate.rotateImage(-1)
		# 	time.sleep(0.01)
		self._controller.setLed(0, 255, 0, 0, 200)
		self._controller.setLed(3, 255, 0, 0, 50)
		self._controller.setLed(6, 255, 0, 0, 25)
		self._controller.setLed(9, 255, 0, 0, 10)
		self._controller.show()


	def onStart(self, *args):
		self._animationTemplate.relayRace([0, 0, 255, 150], relayColor=[255, 0, 0, 200], backgroundColor=[0, 255, 0, 50], speed=-25)
		#self._animationTemplate.rotate(color=[255, 0, 0, 100], speed=25, trail=4)
		#elf._controller.think()
