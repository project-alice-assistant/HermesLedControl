#!/usr/bin/python
import logging

class Interface(object):

	def __init__(self, numLeds):
		self._numLeds 	= numLeds

		self._logger 	= logging.getLogger('HermesLedControl')
		self._leds 		= None
		self._power 	= None
		self._doa 		= False

	@property
	def leds(self):
		return self._leds

	@property
	def numLeds(self):
		return self._numLeds

	@property
	def doa(self):
		return self._doa

	def setPixel(self, ledNum, red, green, blue, brightness):
		pass # Superseeded
	def setPixelRgb(self, ledNum, color, brightness):
		pass # Superseeded
	def clearStrip(self):
		pass # Superseeded
	def show(self):
		self._leds.show()
	def setVolume(self, volume):
		pass # Superseeded
	def setVadLed(self, state):
		pass # Superseeded

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
