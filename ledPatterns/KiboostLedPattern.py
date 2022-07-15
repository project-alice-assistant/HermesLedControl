###########################################################################################################
# SUBMIT YOUR OWN CUSTOM PATTERN AND SHARE WITH THE WORLD YOUR LED ANIMATIONS!
# Visit https://github.com/project-alice-assistant/HermesLedControl/issues/new?template=custom-pattern-proposal.md
# for more information
#
# Check models/LedPattern.py for the available functions
# Do NEVER have a function call a super class function directly!!
# It could cause a deadlock! Instead, call self._controller.THE_METHOD_YOU_WANT
#
# @author: Kiboost
# @weblink: github.com/KiboOst
# @email:
#
###########################################################################################################

import time
from typing import List, Optional

from models.LedPattern import LedPattern
from models.LedsController import LedsController


class KiboostLedPattern(LedPattern):

	def __init__(self, controller: LedsController):
		super(KiboostLedPattern, self).__init__(controller)


	def breathLeds(self, duration: float = 1.0, color: Optional[List] = None, leds: Optional[List] = None):
		"""
		Smooth light up and down, all or specified leds
		duration in seconds
		color as array [r,g,b]
		leds as array of index
		"""
		if not leds:
			leds = list(range(self._numLeds))
		if color is None:
			color = [0, 0, 40]

		pause = float(duration / 200.00)
		direction = 1
		brightness = 0

		frame = 0.0
		while frame < duration and self._animation.is_set():
			for l in leds:
				self._controller.setLed(l, color[0], color[1], color[2], brightness)

			self._controller.show()

			time.sleep(pause)

			if brightness <= 0:
				direction = 1
			elif brightness >= self._controller.defaultBrightness:
				direction = -1

			brightness += direction
			frame += pause


	def tailTranslate(self, duration: float = 0.5, color: Optional[List] = None, invert: bool = False):
		"""
		Progressive translation of all leds.
		duration in seconds
		color as array [r,g,b]
		invert as boolean
		for a ping-pong effect call it twice, second call with invert True
		"""
		if color is None:
			color = [0, 0, 40]

		pause = float(duration / (self._numLeds * 2))
		step = int(100 / self._numLeds + 1)

		for i in range(self._numLeds):
			self._controller.setLed(i, color[0], color[1], color[2], 0)
		self._controller.show()

		refs = [100] + [0] * (self._numLeds - 1)

		for i in range(self._numLeds):
			if not self._animation.is_set():
				break
			for j in range(i, 0, -1):
				if refs[j] >= step:
					refs[j - 1] = refs[j] - step
				else:
					refs[j - 1] = 0

			self._setLedLoop(color, refs, invert)

			if self._animation.is_set():
				time.sleep(pause)
			refs.pop()
			refs.insert(0, 0)

		for _ in range(self._numLeds):
			if not self._animation.is_set():
				break

			self._setLedLoop(color, refs, invert)
			refs.pop()
			refs.insert(0, 0)
			if self._animation.is_set():
				time.sleep(pause)


	def _setLedLoop(self, color: List, refs: List, invert: bool):
		if invert:
			refs = list(reversed(refs))

		for led in range(self._numLeds):
			self._controller.setLed(led, color[0], color[1], color[2], refs[led])
		self._controller.show()


	def translate(self, duration: float = 0.5, color: Optional[List] = None, leds: Optional[List] = None, invert: bool = False):
		"""
		Translation of all or specified leds
		duration in seconds
		color as array [r,g,b]
		leds as array of index
		"""
		if not leds:
			leds = [int(self._numLeds / 2)]
		if color is None:
			color = [0, 0, 40]

		pause = float(duration / (self._numLeds + 1))
		refs = [100 if i in leds else 0 for i in range(self._numLeds)]

		for _ in range(self._numLeds + 1):
			if not self._animation.is_set():
				break
			if invert:
				refs = list(reversed(refs))
			for l in range(self._numLeds):
				self._controller.setLed(l, color[0], color[1], color[2], refs[l])
				self._controller.show()
			if invert:
				refs = list(reversed(refs))
			if self._animation.is_set():
				time.sleep(pause)
			refs.pop()
			refs.insert(0, 0)


	def wakeup(self, *args):
		self.off()
		self._animation.set()
		self.tailTranslate(0.3, [100, 0, 0])
		self.tailTranslate(0.3, [100, 0, 0], True)


	def listen(self, *args):
		self.off()
		self._animation.set()
		while self._animation.is_set():
			self.tailTranslate(0.5, [0, 0, 100])
			self.tailTranslate(0.5, [0, 0, 100], True)


	def think(self, *args):
		self.off()
		self._animation.set()
		while self._animation.is_set():
			self.tailTranslate(0.3, [100, 60, 5])
			self.tailTranslate(0.3, [100, 60, 5], True)


	def speak(self, *args):
		self.off()
		self._animation.set()
		# break for tts without siteid
		i = 0
		while self._animation.is_set():
			self.tailTranslate(0.5, [0, 100, 0])
			self.tailTranslate(0.5, [0, 100, 0], True)
			i += 1
			if i > 7:
				self.idle()
				break


	def idle(self, *args):
		self.off()
		self._animation.set()
		while self._animation.is_set():
			self.breathLeds(1, [0, 0, 75])


	########## DO NEVER CALL CustomLedPattern functions past this line ###########
	def onError(self, *args):
		for i in range(self._numLeds):
			self._controller.setLed(i, 120, 0, 0, self._controller.defaultBrightness)
		self._controller.show()
		time.sleep(0.5)


	def onSuccess(self, *args):
		for i in range(self._numLeds):
			self._controller.setLed(i, 0, 120, 0, self._controller.defaultBrightness)
		self._controller.show()
		time.sleep(0.5)


	def onButton1(self, *args):
		self._controller.toggleState()


	def onStart(self, *args):
		self._controller.wakeup()
		self._controller.idle()
