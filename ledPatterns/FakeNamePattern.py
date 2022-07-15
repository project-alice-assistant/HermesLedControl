###########################################################################################################
# SUBMIT YOUR OWN CUSTOM PATTERN AND SHARE WITH THE WORLD YOUR LED ANIMATIONS!
# Visit https://github.com/project-alice-assistant/HermesLedControl/issues/new?template=custom-pattern-proposal.md
# for more information
#
# Check models/LedPattern.py for the available functions
# Do NEVER have a function call a super class function directly!!
# It could cause a deadlock! Instead, call self._controller.THE_METHOD_YOU_WANT
#
# @author: Fake-Name
# @weblink: https://github.com/fake-name
# @email: github@fake-url.com (yes, this is a real email address)
#
###########################################################################################################

import math
import time
from typing import List

from models.LedPattern import LedPattern
from models.LedsController import LedsController


class FakeNamePattern(LedPattern):

	RED_THETA = 0.0
	ORANGE_THETA = 30.0 / 360
	YELLOW_THETA = 60.0 / 360
	GREEN_THETA = 120.0 / 360
	CYAN_THETA = 180.0 / 360
	BLUE_THETA = 240.0 / 360
	MAGENTA_THETA = 300.0 / 360

	def __init__(self, controller: LedsController):
		super().__init__(controller)
		self._image: List = []


	def _newRainbow(self):
		# Generate a full rotation of the HSV colorspace across the available
		# LEDs.
		self._image = []
		for i in range(self._numLeds):
			red, green, blue = self._hueAngleToRgb((i - 1) / self._numLeds)
			self._image.append([red, green, blue, self._controller.defaultBrightness])


	def _newSingleColor(self, hueAngle: float):
		# Generate a nice full-brightness-off-full-brightness cycle of a
		# specific color across the available LEDs
		self._image = []
		step = math.pi / self._numLeds
		for i in range(self._numLeds):

			r, g, b = self._hueAngleToRgb(hueAngle, value=math.sin(i * step))
			self._image.append([r, g, b, self._controller.defaultBrightness])


	def _rotateImage(self, steps: int):
		if steps < 0:
			for _ in range(0, steps, -1):
				insertBack = self._image.pop(0)
				self._image.insert(len(self._image), insertBack)
		else:
			for _ in range(steps):
				insertBack = self._image.pop()
				self._image.insert(0, insertBack)


	def _displayImage(self):
		for i, led in enumerate(self._image):
			self._controller.setLedRGB(i, led)
		self._controller.show()


	def wakeup(self):
		self._newRainbow()

		for _ in range(self._numLeds):
			self._rotateImage(1)
			self._displayImage()
			time.sleep(0.05)


	def listen(self):
		self._newSingleColor(self.ORANGE_THETA)
		self._animation.set()
		while self._animation.is_set():
			self._rotateImage(1)
			self._displayImage()
			time.sleep(0.05)


	def think(self):
		self._newSingleColor(self.BLUE_THETA)
		self._animation.set()
		while self._animation.is_set():
			self._rotateImage(-1)
			self._displayImage()
			time.sleep(0.05)


	def speak(self):
		self._newSingleColor(self.YELLOW_THETA)
		self._animation.set()
		while self._animation.is_set():
			self._rotateImage(1)
			self._displayImage()
			time.sleep(0.05)
		self.off()


	def onSuccess(self):
		self._newSingleColor(self.GREEN_THETA)
		for _ in range(self._numLeds):
			self._rotateImage(1)
			self._displayImage()
			time.sleep(0.05)
		self.off()


	def onError(self):
		self._newSingleColor(self.RED_THETA)
		for _ in range(self._numLeds):
			self._rotateImage(1)
			self._displayImage()
			time.sleep(0.05)
		self.off()


	def onStart(self, *args):
		self._controller.wakeup()
		self.off()
