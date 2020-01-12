###########################################################################################################
# SUBMIT YOUR OWN CUSTOM PATTERN AND SHARE WITH THE WORLD YOUR LED ANIMATIONS!
# Visit https://github.com/project-alice-assistant/HermesLedControl/issues/new?template=custom-pattern-proposal.md
# for more informations
#
# Check models/LedPattern.py for the available functions
# Do NEVER have a function call a super class function directly!!
# It could cause a deadlock! Instead, call self._controller.THE_METHOD_YOU_WANT
#
# @author: Psychokiller1888
# @weblink: https://projectalice.io
# @email: laurentchervet@bluewin.ch
#
###########################################################################################################
import time

from models.LedPattern import LedPattern

class ProjectAlicePattern(LedPattern):

	def __init__(self, controller):
		super().__init__(controller)
		self._dnd = False


	def wakeup(self, *args):
		start = self._controller.doa()
		self.off()
		self._animator.doubleSidedFilling(color=[255, 255, 255, 15], startAt=start, direction=1, speed=50)
		time.sleep(0.1)
		self._animator.doubleSidedFilling(color=[0, 0, 255, 25], startAt=start, direction=-1, speed=50)
		time.sleep(0.2)
		self._animator.doubleSidedFilling(color=[0, 0, 0, 0], startAt=start, direction=1, speed=50)


	def listen(self, *args):
		start = self._controller.doa()
		self._animator.doubleSidedFilling(color=[0, 0, 255, 25], startAt=start, direction=1, speed=50)
		self._animator.breath(color=[0, 0, 255, 25], minBrightness=2, maxBrightness=25, speed=20)


	def think(self, *args):
		self._animator.rotate(color=[0, 0, 255, 25], speed=20, trail=int(self.numLeds / 3))


	def speak(self, *args):
		self._animator.breath(color=[255, 255, 255, 2], minBrightness=2, maxBrightness=20, speed=40)


	def idle(self):
		self.off()


	def onError(self, *args):
		self._animator.blink(color=[255, 0, 0, 2], minBrightness=2, maxBrightness=20, speed=300, repeat=3)
		self.off()


	def onSuccess(self, *args):
		self._animator.blink(color=[0, 0, 255, 2], minBrightness=2, maxBrightness=25, speed=320, repeat=3)
		self.off()


	def updating(self, *args):
		image = [
			[255, 0, 0, 2],
			[255, 0, 0, 40],
			[255, 0, 0, 100],
			[255, 0, 0, 40],
			[255, 0, 0, 2]
		]

		if len(image) < self._numLeds:
			for _ in range(self.numLeds - len(image)):
				image.append([0, 0, 0, 0])

		self._animator.new(image=image)
		self.animation.set()
		while self.animation.isSet():
			self._animator.rotateImage(-1)
			time.sleep(0.05)


	def setupMode(self, *args):
		self._animator.doublePingPong(color=[0, 0, 255, 10], speed=20)


	def dnd(self, *args):
		self._animator.blink(color=[64, 0, 0, 2], minBrightness=2, maxBrightness=25, speed=250, repeat=5)
		for i in range(self.numLeds - 1):
			self._controller.setLedRGB(ledNum=i, color=[64, 0, 0], brightness=1)
		self._controller.show()


	def conError(self, *args):
		image = [
			[16, 0, 0, 2],
			[255, 0, 0, 100],
			[16, 0, 0, 2]
		]

		if len(image) < self._numLeds:
			for _ in range(self.numLeds - len(image)):
				image.append([0, 0, 0, 0])

		self._animator.new(image=image)
		self.animation.set()
		while self.animation.isSet():
			self._animator.rotateImage(1)
			time.sleep(0.085)


	def message(self, *args):
		self._animator.breath(color=[255, 255, 0, 2], minBrightness=2, maxBrightness=8, speed=8)


	def call(self, *args):
		self.animation.set()
		while self.animation.isSet():
			self._animator.blink(color=[255, 255, 0, 2], minBrightness=2, maxBrightness=8, speed=40, repeat=5)
			time.sleep(1)


	def onStart(self, *args):
		self.wakeup()


	def onButton1(self, *args):
		if self._dnd:
			self._controller.clearLeds()
		else:
			self._controller.dnd()

		self._dnd = not self._dnd
