# -*- coding: utf-8 -*-

###########################################################################################################
# SUBMIT YOUR OWN CUSTOM PATTERN AND SHARE WITH THE WORLD YOUR LED ANIMATIONS!
# Visit https://github.com/Psychokiller1888/snipsLedControl/issues/new?template=custom-pattern-proposal.md
# for more informations
#
# Check models/LedPattern.py for the available functions
# Do NEVER have a function call a super class function directly!!
# It could cause a deadlock! Instead, call self._controller.THE_METHOD_YOU_WANT
#
# @author:
# @weblink:
# @email:
#
###########################################################################################################

from models.LedPattern import LedPattern

class CustomLedPattern(LedPattern):

	def __init__(self, controller):
		super(CustomLedPattern, self).__init__(controller)


	def onStart(self, *args):
		self._logger.warning('Implement me! /ledPatterns/CustomLedPattern.py')