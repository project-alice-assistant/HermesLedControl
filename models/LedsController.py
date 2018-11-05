#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.Interfaces 				import Interfaces
from models.SnipsLedControl 		import *
import logging
import threading
import time

try:
	import queue 					as Queue
except ImportError:
	import Queue 					as Queue

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
		self._interface = None
		self._running 	= False

		self._active = threading.Event()
		if self._params.defaultState == 'on':
			self._active.set()
		else:
			self._active.clear()


		if self._params.pattern == 'google':
			self._pattern = GoogleHomeLedPattern(self)
		elif self._params.pattern == 'alexa':
			self._pattern = AlexaLedPattern(self)
		else:
			self._pattern = CustomLedPattern(self)

		if not self.initHardware():
			self._logger.fatal("Couldn't start hardware")
			self._mainClass.onStop()
			return


		self._buttonsThread = None
		if 'extras' in self._hardware and 'buttons' in self.hardware['extras']:
			import RPi.GPIO
			RPi.GPIO.setmode(RPi.GPIO.BCM)
			for button in self._hardware['extras']['buttons']:
				RPi.GPIO.setup(int(self._hardware['extras']['buttons'][button]['bcm_gpio']), RPi.GPIO.IN)

			self._buttonsThread = threading.Thread(target=self._runButtons)
			self._buttonsThread.setDaemon(True)


		self._queue = Queue.Queue()
		self._animationThread = threading.Thread(target=self._runAnimation)
		self._animationThread.setDaemon(True)


	@property
	def active(self):
		return self._active.isSet()


	@property
	def hardware(self):
		return self._hardware


	def initHardware(self):
		if self._hardware['interface'] == Interfaces.APA102:
			from interfaces.apa102 import APA102
			self._interface = APA102(numLed=self._hardware['numberOfLeds'])

		elif self._hardware['interface'] == Interfaces.NEOPIXELS:
			from interfaces.neopixels import Neopixels
			self._interface = Neopixels(numLeds=self._hardware['numberOfLeds'], pin=self._hardware['gpioPin'])

		elif self._hardware['interface'] == Interfaces.RESPEAKER_MIC_ARRAY_V2:
			from interfaces.respeakerMicArrayV2 import RespeakerMicArrayV2
			self._interface = RespeakerMicArrayV2(numLeds=self._hardware['numberOfLeds'], vid=self._hardware['vid'], pid=self._hardware['pid'])

		elif self._hardware['interface'] == Interfaces.MATRIX_VOICE:
			from interfaces.matrixvoice import MatrixVoice
			self._interface = MatrixVoice(numLeds=self._hardware['numberOfLeds'], matrixIp=self._hardware['matrixIp'], everloopPort=self._hardware['everloopPort'])

		if self._interface is None:
			return False
		else:
			return True


	def wakeup(self):
		if self._params.wakeupPattern is None:
			self._put(self._pattern.wakeup)
		else:
			try:
				func = getattr(self._pattern, self._params.wakeupPattern)
				self._put(func)
			except AttributeError:
				self._logger.error("Can't find {} method in pattern".format(self._params.wakeupPattern))


	def listen(self):
		if self._params.listenPattern is None:
			self._put(self._pattern.listen)
		else:
			try:
				func = getattr(self._pattern, self._params.listenPattern)
				self._put(func)
			except AttributeError:
				self._logger.error("Can't find {} method in pattern".format(self._params.listenPattern))


	def think(self):
		if self._params.thinkPattern is None:
			self._put(self._pattern.think)
		else:
			try:
				func = getattr(self._pattern, self._params.thinkPattern)
				self._put(func)
			except AttributeError:
				self._logger.error("Can't find {} method in pattern".format(self._params.thinkPattern))


	def speak(self):
		if self._params.speakPattern is None:
			self._put(self._pattern.speak)
		else:
			try:
				func = getattr(self._pattern, self._params.speakPattern)
				self._put(func)
			except AttributeError:
				self._logger.error("Can't find {} method in pattern".format(self._params.speakPattern))


	def idle(self):
		if self._params.idlePattern is None:
			self._put(self._pattern.idle)
		else:
			try:
				func = getattr(self._pattern, self._params.idlePattern)
				self._put(func)
			except AttributeError:
				self._logger.error("Can't find {} method in pattern".format(self._params.idlePattern))


	def onError(self):
		if self._params.errorPattern is None:
			self._put(self._pattern.onError)
		else:
			try:
				funct = getattr(self._pattern, self._params.errorPattern)
				self._put(funct)
			except AttributeError:
				self._logger.error("Can't find {} method in pattern".format(self._params.errorPattern))


	def onSuccess(self):
		if self._params.successPattern is None:
			self._put(self._pattern.onSuccess)
		else:
			try:
				func = getattr(self._pattern, self._params.successPattern)
				self._put(func)
			except AttributeError:
				self._logger.error("Can't find {} method in pattern".format(self._params.successPattern))


	def off(self):
		if self._params.offPattern is None:
			self._put(self._pattern.off, True)
		else:
			try:
				func = getattr(self._pattern, self._params.offPattern)
				self._put(func, True)
			except AttributeError:
				self._logger.error("Can't find {} method in pattern".format(self._params.offPattern))


	def toggleStateOff(self):
		if self.active:
			threading.Timer(interval=0.5, function=self._clear).start()
		self.off()


	def _clear(self):
		self._active.clear()


	def toggleStateOn(self):
		if not self.active:
			threading.Timer(interval=0.5, function=self._pattern.onStart).start()
		self._active.set()


	def toggleState(self):
		if self.active:
			self.toggleStateOff()
		else:
			self.toggleStateOn()


	def _put(self, func, flush=False):
		self._pattern.animation.clear()

		if not self.active:
			return

		if flush:
			self._queue.empty()

		self._queue.put(func)


	def _runAnimation(self):
		while self._running:
			self._pattern.animation.clear()
			func = self._queue.get()
			func()


	def setLed(self, ledNum, red, green, blue, brightness=100):
		self._interface.setPixel(ledNum, red, green, blue, brightness)


	def setLedRGB(self, ledNum, color, brightness=100):
		self._interface.setPixelRgb(ledNum, color, brightness)


	def clearLeds(self):
		self._interface.clearStrip()


	@DeprecationWarning
	def showData(self, data):
		"""Will soon be removed in favor or more understandable and per led setting"""
		for i in range(self._hardware['numberOfLeds']):
			self.setLed(i, int(data[4 * i + 1]), int(data[4 * i + 2]), int(data[4 * i + 3]))
		self.show()


	def show(self):
		self._interface.show()


	def _runButtons(self):
		while self._running:
			try:
				for button in self._hardware['extras']['buttons']:
					state = GPIO.input(self._hardware['extras']['buttons'][button]['bcm_gpio'])
					if not state:
						try:
							func = getattr(self._pattern, self._hardware['extras']['buttons'][button]['function'])
							func()
						except AttributeError:
							self._logger.error("Function {} couldn't be found in pattern")
				time.sleep(0.25)
			except:
				import RPi.GPIO as GPIO


	def onStart(self):
		if self._interface is None:
			return

		self._running = True
		self._interface.onStart()
		self._pattern.onStart()
		self._buttonsThread.start()
		self._animationThread.start()


	def onStop(self):
		self._pattern.animation.clear()
		self._pattern.onStop()

		self._running = False
		self._interface.onStop()

		self._animationThread.join(timeout=2)
		if self._buttonsThread is not None:
			self._buttonsThread.join(timeout=2)
