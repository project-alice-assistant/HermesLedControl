import time

from models.LedPattern import LedPattern
from models.LedsController import LedsController


class AlexaLedPattern(LedPattern):

	def __init__(self, controller: LedsController):
		super(AlexaLedPattern, self).__init__(controller)

		self._colors = {
			'blank' : (0, 0, 0),
			'blue'  : (0, 0, 255),
			'red'   : (60, 0, 0),
			'yellow': (255, 255, 0),
			'white' : (255, 255, 255)
		}


	def wakeup(self, direction = 0):
		brightness = max(5, self._controller.defaultBrightness - 50)
		for i in range(int(round(self._numLeds / 2)) + 1):
			brightness += 5
			self._controller.setLedRGB(i, self._colors['white'], brightness)

			if i > 0:
				self._controller.setLedRGB(self._numLeds - i, self._colors['white'], brightness)

			if i > 1:
				self._controller.setLedRGB(i - 2, self._colors['blue'], brightness)
				if i > 2:
					self._controller.setLedRGB(self._numLeds - i + 2, self._colors['blue'], brightness)

			self._controller.show()
			time.sleep(0.02)
		time.sleep(0.5)


	def listen(self):
		""" there is no listen animation for this led pattern """
		return


	def think(self):
		first = self._colors['blue']
		second = self._colors['white']

		self._animation.set()
		while self._animation.is_set():
			for i in range(1, self._numLeds + 1):
				if not self._animation.is_set():
					break

				if i % 2 == 0:
					self._controller.setLedRGB(i - 1, first)
				else:
					self._controller.setLedRGB(i - 1, second)

			self._controller.show()

			if first == self._colors['blue']:
				first = self._colors['white']
				second = self._colors['blue']
			else:
				first = self._colors['blue']
				second = self._colors['white']

			time.sleep(0.15)


	def speak(self):
		direction = 1
		red = 255
		green = 255

		for i in range(self._numLeds):
			self._controller.setLedRGB(i, self._colors['white'])

		self._animation.set()
		while self._animation.is_set():
			for i in range(self._numLeds):
				if not self._animation.is_set():
					break
				self._controller.setLed(i, red=red, green=green, blue=255)
			self._controller.show()

			red -= direction
			green -= direction
			if red >= 255 or red <= 0:
				direction *= -1

			time.sleep(0.002)


	def off(self, *args):
		for i in range(int(round(self._numLeds / 2)) + 1):
			self._controller.setLedRGB(i, self._colors['blank'], 0)
			self._controller.setLedRGB(self._normalizeIndex(self._numLeds - i), self._colors['blank'], 0)

			self._controller.show()
			time.sleep(0.02)


	def idle(self, *args):
		self.off()


	def onButton1(self, *args):
		# When mic mute button pressed
		for i in range(self._numLeds):
			self._controller.setLed(i, 60, 0, 0)
		self._controller.show()


	def onStart(self, *args):
		self._controller.wakeup()
		self._controller.idle()
