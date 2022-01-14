import logging
from typing import List


class Interface(object):

	def __init__(self, numLeds: int):
		self._numLeds = numLeds

		self._logger = logging.getLogger('HermesLedControl')
		self._leds = None
		self._power = None
		self._doa = False


	@property
	def leds(self):
		return self._leds


	@property
	def numLeds(self) -> int:
		return self._numLeds


	@property
	def doa(self) -> bool:
		return self._doa


	def setPixel(self, ledNum: int, red: int, green: int, blue: int, brightness: int):
		pass  # Superseeded


	def setPixelRgb(self, ledNum: int, color: List, brightness: int):
		pass  # Superseeded


	def clearStrip(self):
		pass  # Superseeded


	def show(self):
		self._leds.show()


	def setVolume(self, volume: int):
		pass  # Superseeded


	def setVadLed(self, state: int):
		pass  # Superseeded


	def onStart(self):
		if self._power is not None:
			try:
				self._power.on()
			except:
				try:
					self._power.write(0)
				except:
					pass


	def onStop(self):
		if self._power is not None:
			try:
				self._power.off()
			except:
				try:
					self._power.write(1)
				except:
					pass
