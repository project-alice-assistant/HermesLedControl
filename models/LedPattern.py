from models.Animations import Animations
from models.LedsController import *
import logging
import threading

class LedPattern:

	def __init__(self, controller):
		self._logger 				= logging.getLogger('HermesLedControl')
		self._controller 			= controller # type: LedsController
		self._numLeds 				= self._controller.interface.numLeds
		self._animation 			= threading.Event()
		self._animator 				= Animations(self._animation, controller)


	@property
	def animation(self):
		return self._animation


	@property
	def numLeds(self):
		return self._numLeds


	def nothing(self, *args) 	: pass
	def wakeup(self, *args)		: pass
	def listen(self, *args)		: pass
	def think(self, *args)		: pass
	def speak(self, *args)		: pass
	def idle(self, *args)		: pass
	def off(self, *args)		: self._controller.clearLeds()
	def onError(self, *args)	: pass
	def onSuccess(self, *args)	: pass
	def updating(self, *args)	: pass
	def call(self, *args)		: pass
	def setupMode(self, *args)	: pass
	def conError(self, *args)	: pass
	def message(self, *args)	: pass
	def dnd(self, *args)		: pass
	def onVolumeSet(self, *args): pass
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


	def _normalizeIndex(self, index):
		"""
		Makes sure the given index is valid in the led strip or returns the one on the other side of the loop
		:param int index:
		:return: int
		"""
		if index < 0:
			return self._numLeds - abs(index)
		elif index >= self._numLeds:
			return index - self._numLeds
		else:
			return index
