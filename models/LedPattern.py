import colorsys
import logging
from threading import Event
from typing import Tuple

from models.Animations import Animations
from models.LedsController import LedsController


class LedPattern(object):

	def __init__(self, controller: LedsController):
		self._logger = logging.getLogger('HermesLedControl')
		self._controller: LedsController = controller
		self._numLeds = self._controller.interface.numLeds
		self._animation: Event= Event()
		self._animator: Animations = Animations(self._animation, controller)


	@property
	def animator(self) -> Animations:
		return self._animator


	@property
	def animation(self) -> Event:
		return self._animation


	@property
	def numLeds(self) -> int:
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
	def off(self, *args):
		self._controller.clearLeds()
	def onError(self, *_args):
		pass # Superseeded
	def onSuccess(self, *_args):
		pass # Superseeded
	def onVolumeSet(self, *_args):
		pass # Superseeded
	def onButton1(self, *args): #NOSONAR
		self._logger.warning('Button 1 not implemented, override it in CustomLedPattern')
	def onButton2(self, *_args): #NOSONAR
		self._logger.warning('Button 2 not implemented, override it in CustomLedPattern')
	def onButton3(self, *_args): #NOSONAR
		self._logger.warning('Button 3 not implemented, override it in CustomLedPattern')
	def onButton4(self, *_args): #NOSONAR
		self._logger.warning('Button 4 not implemented, override it in CustomLedPattern')
	def onButton5(self, *_args): #NOSONAR
		self._logger.warning('Button 5 not implemented, override it in CustomLedPattern')
	def onButton6(self, *_args): #NOSONAR
		self._logger.warning('Button 6 not implemented, override it in CustomLedPattern')
	def onStart(self, *_args):
		pass # Superseeded
	def onStop(self, *_args):
		self.off()


	@staticmethod
	def color(red, green, blue, white=0):
		return (white << 24) | (red << 16) | (green << 8) | blue


	def _normalizeIndex(self, index: int):
		"""
		Makes sure the given index is valid in the LED strip or returns the one on the other side of the loop
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
	def _hueAngleToRgb(angle, saturation: int = 1, value: float = 1.0) -> Tuple[int, int, int]:
		"""
		Given a hue angle, return the RGB triplet
		that represents the 100% saturated rgb value
		for that Hue from the HSV color model.
		Input value is 0-1.
		Return value is normalized to 0-255 integer range
		:param int saturation:
		:param float value:
		:return: int
		"""

		red, green, blue = colorsys.hsv_to_rgb(angle % 1, saturation, value)
		ret = int(red * 255), int(green * 255), int(blue * 255)
		return ret
