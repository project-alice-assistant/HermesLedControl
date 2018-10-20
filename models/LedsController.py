#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.Interfaces 			import Interfaces
from models.SnipsLedControl 	import *
import logging
import threading
from gpiozero 					import LED

try:
	import queue 				as Queue
except ImportError:
	import Queue 				as Queue

from ledPatterns.AlexaLedPattern 	import AlexaLedPattern
from ledPatterns.CustomLedPattern 	import CustomLedPattern
from ledPatterns.GoogleLedPattern 	import GoogleHomeLedPattern


class LedsController:
	INSTANCE = None

	def __init__(self, mainClass):
		self._logger = logging.getLogger('SnipsLedControl')
		self._logger.info('Initializing leds controller')

		self._mainClass = mainClass # type: SnipsLedControl

		if self.INSTANCE is None:
			self.INSTANCE = self
		else:
			self._logger.fatal('Trying to instanciate LedsController but instance already exists')
			self._mainClass.onStop()

		self._params 	= self._mainClass.params
		self._hardware 	= self._mainClass.hardware
		self._interface = self._hardware['interface']

		if self._params.pattern == 'google':
			self._pattern = GoogleHomeLedPattern(self)
		elif self._params.pattern == 'alexa':
			self._pattern = AlexaLedPattern(self)
		else:
			self._pattern = CustomLedPattern(self)

		self._power = None
		if self._interface == Interfaces.APA102:
			from interfaces.apa102 import APA102
			self._power = LED(5)
			self._power.on()
			self._interface = APA102(num_led=self._hardware['numberOfLeds'])
		elif self._interface == Interfaces.NEOPIXELS:
			from interfaces.neopixels import Neopixels
			self._interface = Neopixels(numLeds=self._hardware['numberOfLeds'], pin=self._hardware['pin'])
		elif self._interface == Interfaces.RESPEAKER_MIC_ARRAY_V2:
			from interfaces.respeakerMicArrayV2 import RespeakerMicArrayV2
			self._power = LED(5)
			self._power.on()
			self._interface = RespeakerMicArrayV2(numLeds=self._hardware['numberOfLeds'], vid=self._hardware['vid'], pid=self._hardware['pid'])

		if self._interface is None:
			self._logger.fatal("Couldn't start hardware")
			self._mainClass.onStop()
			return

		self._running = False

		self._active = True if self._params.defaultState == 'on' else False

		self._queue = Queue.Queue()
		self._thread = threading.Thread(target=self._run)
		self._thread.daemon = True
		self._thread.start()

		self._lastDirection = None


	@property
	def active(self):
		return self._active


	@property
	def hardware(self):
		return self._hardware


	def wakeup(self):
		if self._params.wakeupPattern is None:
			print('ici')
			self.put(self._pattern.wakeup)
		else:
			print('la')
			func = getattr(self._pattern, self._params.wakeupPattern)
			self.put(func)


	def listen(self):
		if self._params.listenPattern is None:
			self.put(self._pattern.listen)
		else:
			func = getattr(self._pattern, self._params.listenPattern)
			self.put(func)


	def think(self):
		if self._params.thinkPattern is None:
			self.put(self._pattern.think)
		else:
			func = getattr(self._pattern, self._params.thinkPattern)
			self.put(func)


	def speak(self):
		if self._params.speakPattern is None:
			self.put(self._pattern.speak)
		else:
			func = getattr(self._pattern, self._params.speakPattern)
			self.put(func)


	def idle(self):
		if self._params.idlePattern is None:
			self.put(self._pattern.idle)
		else:
			func = getattr(self._pattern, self._params.idlePattern)
			self.put(func)


	def onError(self):
		if self._params.errorPattern is None:
			self.put(self._pattern.onError)
		else:
			funct = getattr(self._pattern, self._params.errorPattern)
			self.put(funct)


	def onSuccess(self):
		if self._params.successPattern is None:
			self.put(self._pattern.onSuccess)
		else:
			func = getattr(self._pattern, self._params.successPattern)
			self.put(func)


	def off(self):
		if self._params.offPattern is None:
			self.put(self._pattern.off)
		else:
			func = getattr(self._pattern, self._params.offPattern)
			self.put(func)


	def toggleStateOff(self):
		self._active = False
		self.off()


	def toggleStateOn(self):
		self._active = True


	def toggleState(self):
		if self._active:
			self._active = False
			self.off()
		else:
			self._active = True


	def put(self, func):
		self._pattern.animation.clear()

		if not self._active:
			return

		self._queue.put(func)


	def _run(self):
		while self._running:
			self._pattern.stop = False
			func = self._queue.get()
			func()


	def setLed(self, ledNum, red, green, blue, brightness=100):
		self._interface.set_pixel(ledNum, red, green, blue, brightness)


	def setLedRGB(self, ledNum, rgb, brightness=100):
		self._interface.set_pixel_rgb(ledNum, rgb, brightness)


	def clearLeds(self):
		self._interface.clear_strip()


	def showData(self, data):
		for i in range(self._hardware['numberOfLeds']):
			self.setLed(i, int(data[4 * i + 1]), int(data[4 * i + 2]), int(data[4 * i + 3]))


	def show(self):
		self._interface.show()


	def onStart(self):
		self._running = True


	def onStop(self):
		self._pattern.stop = True
		self._pattern.off()

		self._queue.empty()

		self._running = False
		self._thread.join()

		if self._power is not None:
			self._power.off()
