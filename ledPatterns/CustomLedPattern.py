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


	def onStart(self, *args):
		#self._animationTemplate.doublePingPong(color=[255, 0, 0, 100], speed=25, startAt=0)
		#self._animationTemplate.relayRace([0, 0, 255, 150], relayColor=[255, 0, 0, 200], backgroundColor=[0, 255, 0, 50], speed=-25)
		self._animationTemplate.waitWheel([0, 0, 255, 150], backgroundColor=[0, 0, 0, 0], speed=35)
		#self._animationTemplate.rotate(color=[100, 0, 0, 50], speed=10, trail=2)
