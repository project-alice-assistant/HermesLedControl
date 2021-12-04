###########################################################################################################
# SUBMIT YOUR OWN CUSTOM PATTERN AND SHARE WITH THE WORLD YOUR LED ANIMATIONS!
# Visit https://github.com/project-alice-assistant/HermesLedControl/issues/new?template=custom-pattern-proposal.md
# for more informations
#
# Check models/LedPattern.py for the available functions
# Do NEVER have a function call a super class function directly!!
# It could cause a deadlock! Instead, call self._controller.THE_METHOD_YOU_WANT
#
# @author: JRK
# @weblink: github.com/jr-k
# @email:
#
###########################################################################################################

from models.LedPattern import LedPattern
from models.LedsController import LedsController


class PgasPattern(LedPattern):

	def __init__(self, controller: LedsController):
		super().__init__(controller)
		self._dnd = False


	def showcase(self):
		self.off()


	def wakeup(self, *args):
		self._animator.doublePingPong(color=[0, 0, 255, 255], startAt=0, speed=30, duration=2)


	def listen(self, *args):
		self._animator.breath(color=[0, 0, 255, 25], minBrightness=2, maxBrightness=25, speed=20)


	def think(self, *args):
		self._animator.rotate(color=[0, 0, 255, 25], speed=20, trail=int(self.numLeds / 3))


	def speak(self, *args):
		self._animator.breath(color=[0, 255, 255, 25], minBrightness=2, maxBrightness=25, speed=40)


	def idle(self):
		self.off()


	def onError(self, *args):
		self._animator.blink(color=[255, 0, 0, 2], minBrightness=2, maxBrightness=20, speed=300, repeat=3)


	def onStart(self, *args):
		self._animator.rainbow(brightness=255, speed=500, duration=3)
