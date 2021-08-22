import colorsys

from models.Animations import Animations
from models.LedsController import *


class LedPattern:

	def __init__(self, controller):
		self._logger 				= logging.getLogger('HermesLedControl')
		self._controller 			= controller # type: LedsController
		self._numLeds 				= self._controller.interface.numLeds
		self._animation 			= threading.Event()
		self._animator 				= Animations(self._animation, controller)


	@property
	def animator(self):
		return self._animator


	@property
	def animation(self):
		return self._animation


	@property
	def numLeds(self):
		return self._numLeds


	def nothing(self, *args):
		pass # Superseeded
	def wakeup(self, *args):
		pass # Superseeded
	def listen(self, *args):
		pass # Superseeded
	def think(self, *args):
		pass # Superseeded
	def speak(self, *args):
		pass # Superseeded
	def idle(self, *args):
		pass # Superseeded
	def off(self, *args):
		self._controller.clearLeds()
	def onError(self, *args):
		pass # Superseeded
	def onSuccess(self, *args):
		pass # Superseeded
	def updating(self, *args):
		pass # Superseeded
	def call(self, *args):
		pass # Superseeded
	def setupMode(self, *args):
		pass # Superseeded
	def conError(self, *args):
		pass # Superseeded
	def message(self, *args):
		pass # Superseeded
	def dnd(self, *args):
		pass # Superseeded
	def onVolumeSet(self, *args):
		pass # Superseeded
	def onButton1(self, *args): #NOSONAR
		self._logger.warning('Button 1 not implemented, override it in CustomLedPattern')
	def onButton2(self, *args): #NOSONAR
		self._logger.warning('Button 2 not implemented, override it in CustomLedPattern')
	def onButton3(self, *args): #NOSONAR
		self._logger.warning('Button 3 not implemented, override it in CustomLedPattern')
	def onButton4(self, *args): #NOSONAR
		self._logger.warning('Button 4 not implemented, override it in CustomLedPattern')
	def onButton5(self, *args): #NOSONAR
		self._logger.warning('Button 5 not implemented, override it in CustomLedPattern')
	def onButton6(self, *args): #NOSONAR
		self._logger.warning('Button 6 not implemented, override it in CustomLedPattern')
	def onStart(self, *args):
		pass # Superseeded
	def onStop(self, *args):
		self.off()


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


	@staticmethod
	def _hueAngleToRgb(angle, saturation = 1, value = 1):
		"""
		Given an hue angle, return the RGB triplet
		that represents the 100% saturated rgb value
		for that Hue from the HSV color model.

		Input value is 0-1.
		Return value is normalized to 0-255 integer range

		"""
		# Get fully saturated HSV value
		r, g, b = colorsys.hsv_to_rgb(angle % 1, saturation, value)
		ret = int(r * 255), int(g * 255), int(b * 255)
		return ret
