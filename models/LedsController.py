import queue as Queue
import threading
import uuid
from typing import Callable
import logging

from models.Exceptions import InterfaceInitError
from models.HermesLedControl import *
from models.Interfaces import Interfaces


class LedsController(object):
	INSTANCE = None


	def __init__(self, mainClass):
		self._logger = logging.getLogger('HermesLedControl')
		self._logger.info('Initializing leds controller')

		self._mainClass = mainClass  # type: HermesLedControl

		if self.INSTANCE is None:
			self.INSTANCE = self
		else:
			self._logger.fatal('Trying to instanciate LedsController but instance already exists')
			self._mainClass.onStop()

		self._params = self._mainClass.params
		self._hardware = self._mainClass.hardware
		self._interface = None
		self._running = False
		self._defaultBrightness = self._params.defaultBrightness
		self._stickyAnimation = None
		self._runningRequestId = None

		if not self._params.enableDoA and 'doa' in self._hardware:
			self._hardware['doa'] = False

		self._active = threading.Event()
		if self._params.defaultState == 'on':
			self._active.set()
		else:
			self._active.clear()

		if not self.initHardware():
			self._logger.fatal("Couldn't start hardware")
			self._mainClass.onStop()
			return

		if self._params.pattern == 'google':
			from ledPatterns.GoogleLedPattern import GoogleHomeLedPattern
			self._pattern = GoogleHomeLedPattern(self)
		elif self._params.pattern == 'alexa':
			from ledPatterns.AlexaLedPattern import AlexaLedPattern
			self._pattern = AlexaLedPattern(self)
		elif self._params.pattern == 'kiboost':
			from ledPatterns.KiboostLedPattern import KiboostLedPattern
			self._pattern = KiboostLedPattern(self)
		elif self._params.pattern == 'projectalice':
			from ledPatterns.ProjectAlicePattern import ProjectAlicePattern
			self._pattern = ProjectAlicePattern(self)
		elif self._params.pattern == 'pgas':
			from ledPatterns.PgasPattern import PgasPattern
			self._pattern = PgasPattern(self)
		elif self._params.pattern == 'fake-name':
			from ledPatterns.FakeNamePattern import FakeNamePattern
			self._pattern = FakeNamePattern(self)
		else:
			from ledPatterns.CustomLedPattern import CustomLedPattern
			self._pattern = CustomLedPattern(self)

		self._buttonsThread = None
		if 'extras' in self._hardware and 'buttons' in self.hardware['extras']:
			import RPi.GPIO

			RPi.GPIO.setmode(RPi.GPIO.BCM)
			for button in self._hardware['extras']['buttons']:
				RPi.GPIO.setup(int(self._hardware['extras']['buttons'][button]['bcm_gpio']), RPi.GPIO.IN)

			self._buttonsThread = threading.Thread(target=self._runButtons)
			self._buttonsThread.setDaemon(True)

		self._timeout = 0
		if self._params.timeout and self._params.timeout > 0:
			self._timeout = self._params.timeout

		self._queue = Queue.Queue()
		self._animationThread = threading.Thread(target=self._runAnimation)
		self._animationThread.setDaemon(True)


	@property
	def stickyAnimation(self):
		return self._stickyAnimation


	@stickyAnimation.setter
	def stickyAnimation(self, value):
		self._stickyAnimation = value


	@property
	def active(self):
		return self._active.is_set()


	@property
	def hardware(self):
		return self._hardware


	@property
	def defaultBrightness(self):
		return self._defaultBrightness


	@property
	def interface(self):
		return self._interface


	@property
	def pattern(self):
		return self._pattern


	def initHardware(self):
		try:
			if self._hardware['interface'] == Interfaces.APA102:
				from interfaces.apa102 import APA102

				self._interface = APA102(hardware=self._hardware, endFrame=self._hardware['endFrame'])

			elif self._hardware['interface'] == Interfaces.NEOPIXELS:
				from interfaces.neopixels import Neopixels

				self._interface = Neopixels(numLeds=self._hardware['numberOfLeds'], stripType=self._hardware['type'], pin=self._hardware['gpioPin'])

			elif self._hardware['interface'] == Interfaces.RESPEAKER_MIC_ARRAY_V2:
				from interfaces.respeakerMicArrayV2 import RespeakerMicArrayV2

				self._interface = RespeakerMicArrayV2(hardware=self._hardware, vid=self._hardware['vid'], pid=self._hardware['pid'])

			elif self._hardware['interface'] == Interfaces.RESPEAKER_MIC_ARRAY_V1:
				from interfaces.respeakerMicArrayV1 import RespeakerMicArrayV1

				self._interface = RespeakerMicArrayV1(hardware=self._hardware, vid=self._hardware['vid'], pid=self._hardware['pid'])

			elif self._hardware['interface'] == Interfaces.MATRIX_VOICE:
				from interfaces.matrixvoice import MatrixVoice

				self._interface = MatrixVoice(numLeds=self._hardware['numberOfLeds'])

			elif self._hardware['interface'] == Interfaces.MATRIX_CORE:
				from interfaces.matrixcore import MatrixCore

				self._interface = MatrixCore(numLeds=self._hardware['numberOfLeds'], matrixIp=self._params.matrixIp, everloopPort=self._params.everloopPort)

			elif self._hardware['interface'] == Interfaces.PURE_GPIO:
				from interfaces.pureGPIO import PureGPIO

				self._interface = PureGPIO(numLeds=self._hardware['numberOfLeds'], pinout=self._hardware['gpios'], activeHigh=self._hardware['activeHigh'])

			if self._interface is None:
				return False
			else:
				return True
		except InterfaceInitError as e:
			self._logger.error(f'Interface init error: {e}')
			return False


	def setVolume(self, volume):
		"""
		Some hardware such as respeaker mic array have onboard volume control that can be set
		:type volume: int
		:return:
		"""
		if 'extras' in self._hardware and 'volume' in self._hardware['extras']:
			try:
				minVol = self._hardware['extras']['volume']['min']
				maxVol = self._hardware['extras']['volume']['max']
				volume = max(min(volume, maxVol), minVol)
				if self._interface is not None:
					self._interface.setVolume(volume)
			except:
				self._logger.error('Missing or wrong configuration for volume setting')
		else:
			self._logger.warning('Tried to set volume on an unsupported device')


	def setVadLed(self, state):
		"""
		Some hardware such as respeaker mic array have onboard vad led
		:type state: int (0-1)
		:return:
		"""
		if 'extras' in self._hardware and 'vadLed' in self._hardware['extras']:
			try:
				if self._interface is not None:
					self._interface.setVadLed(state)
			except:
				self._logger.error('Missing or wrong vad led setting')
		else:
			self._logger.warning('Tried to set vad led on an unsupported device')


	def putStickyPattern(self, pattern, patternMethod = None, sticky: bool = False, flush: bool = False, duration: float = 0, **kwargs):
		if sticky:
			self._stickyAnimation = {"func": pattern, "args": kwargs, "duration": duration}

		if patternMethod is None:
			self._put(pattern, flush=flush, duration=duration, **kwargs)
		else:
			try:
				func = getattr(self._pattern, patternMethod)
				self._put(func, flush=flush, duration=duration, **kwargs)
			except AttributeError:
				self._logger.error(f"Can't find {patternMethod} method in pattern")
				self._put(pattern, flush=flush, duration=duration, **kwargs)


	def wakeup(self, sticky: bool = False):
		self.putStickyPattern(self._pattern.wakeup, self._params.wakeupPattern, sticky)


	def listen(self, sticky: bool = False):
		self.putStickyPattern(self._pattern.listen, self._params.listenPattern, sticky)


	def think(self, sticky: bool = False):
		self.putStickyPattern(self._pattern.think, self._params.thinkPattern, sticky)


	def speak(self, sticky: bool = False):
		self.putStickyPattern(self._pattern.speak, self._params.speakPattern, sticky)


	def idle(self):
		if self._stickyAnimation:
			self._put(self._stickyAnimation['func'], flush=False, duration=self._stickyAnimation['duration'], noTimeout=True, **self._stickyAnimation['args'])
		else:
			if self._params.idlePattern is None:
				self._put(self._pattern.idle, noTimeout=True)
			else:
				try:
					func = getattr(self._pattern, self._params.idlePattern)
					self._put(func, noTimeout=True)
				except AttributeError:
					self._logger.error(f"Can't find {self._params.idlePattern} method in pattern")
					self._put(self._pattern.idle, noTimeout=True)


	def onError(self, sticky: bool = False):
		self.putStickyPattern(self._pattern.onError, self._params.errorPattern, sticky)


	def onSuccess(self, sticky: bool = False):
		self.putStickyPattern(self._pattern.onSuccess, self._params.successPattern, sticky)


	def updating(self, sticky: bool = False):
		self.putStickyPattern(self._pattern.updating, self._params.updatingPattern, sticky)


	def call(self, sticky: bool = False):
		self.putStickyPattern(self._pattern.call, self._params.callPattern, sticky)


	def setupMode(self, sticky: bool = False):
		self.putStickyPattern(self._pattern.setupMode, self._params.setupModePattern, sticky)


	def conError(self, sticky: bool = False):
		self.putStickyPattern(self._pattern.conError, self._params.conErrorPattern, sticky)


	def message(self, sticky: bool = False):
		self.putStickyPattern(self._pattern.message, self._params.messagePattern, sticky)


	def dnd(self, sticky: bool = False):
		self.putStickyPattern(self._pattern.dnd, self._params.dndPattern, sticky)


	def off(self):
		if self._params.offPattern is None:
			self._put(self._pattern.off, True)
		else:
			try:
				func = getattr(self._pattern, self._params.offPattern)
				self._put(func, True)
			except AttributeError:
				self._logger.error(f"Can't find {self._params.offPattern} method in pattern")
				self._put(self._pattern.off, True)


	def start(self):
		if self._params.startPattern is None:
			self._put(self._pattern.onStart, True)
		else:
			try:
				func = getattr(self._pattern, self._params.startPattern)
				self._put(func, True)
			except AttributeError:
				self._logger.error(f"Can't find {self._params.startPattern} method in pattern")
				self._put(self._pattern.onStart, True)


	def stop(self):
		if self._params.startPattern is None:
			self._put(self._pattern.onStop, True)
		else:
			try:
				func = getattr(self._pattern, self._params.stopPattern)
				self._put(func, True)
			except AttributeError:
				self._logger.error(f"Can't find {self._params.stopPattern} method in pattern")
				self._put(self._pattern.onStart, True)


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


	def _put(self, func: Callable, flush = False, duration: float = 0, noTimeout: bool = False, **kwargs):
		self._pattern.animation.clear()

		if not self.active:
			return

		if flush:
			self._queue.empty()

		requestId = str(uuid.uuid4())
		self._logger.debug(f'New animation "{func.__name__}" has id {requestId}')

		if not noTimeout and self._timeout and (not duration or duration > self._timeout):
			self._logger.debug(f'Timeout is setting duration from {duration} to {self._timeout}')
			duration = self._timeout

		if duration:
			threading.Timer(interval=int(duration), function=self.scheduledEndAnimation, args=[requestId]).start()

		self._queue.put({"func": func, "args": kwargs, "duration": duration, "requestId": requestId})


	def _runAnimation(self):
		while self._running:
			self._pattern.animation.clear()
			funcRecipe = self._queue.get()
			self._runningRequestId = funcRecipe["requestId"]
			funcRecipe['func'](**funcRecipe['args'])


	def scheduledEndAnimation(self, requestId):
		if self._runningRequestId == requestId:
			self._logger.debug(f'Request {requestId} animation ended or timed out')
			self.idle()


	def setLed(self, ledNum, red, green, blue, brightness = -1):
		if ledNum < 0 or ledNum > self._interface.numLeds:
			self._logger.warning(f"Tried to access a led number that doesn't exist: {ledNum} / {self._interface.numLeds}")
			return

		if brightness == -1:
			brightness = self.defaultBrightness
		self._interface.setPixel(ledNum, red, green, blue, brightness)


	def setLedRGB(self, ledNum, color, brightness = -1):
		if len(color) > 3:
			brightness = color[3]
		elif brightness == -1:
			brightness = self.defaultBrightness

		self.setLed(ledNum, color[0], color[1], color[2], brightness)


	def clearLeds(self):
		if self._interface is not None:
			self._interface.clearStrip()


	@DeprecationWarning
	def showData(self, data):
		"""Will soon be removed in favor or more understandable and per led setting"""
		for i in range(self._hardware['numberOfLeds']):
			self.setLed(i, int(data[4 * i + 1]), int(data[4 * i + 2]), int(data[4 * i + 3]))
		self.show()


	def show(self):
		self._interface.show()


	def doa(self):
		if self._params.enableDoA and self._hardware.get('doa'):
			angle = self._interface.doa()
			if angle > 0:
				return int(round(angle / (360 / self._hardware['numberOfLeds'])))

		return 0


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
			self._logger.error('Interface error')
			return

		self._running = True
		self._interface.onStart()

		self._animationThread.start()
		if self._buttonsThread is not None:
			self._buttonsThread.start()

		threading.Timer(interval=0.5, function=self._pattern.onStart).start()


	def onStop(self):
		self._pattern.animation.clear()
		self._pattern.onStop()

		self._running = False
		self._interface.onStop()

		if self._animationThread is not None and self._animationThread.is_alive():
			self._animationThread.join(timeout=2)
		if self._buttonsThread is not None and self._buttonsThread.is_alive():
			self._buttonsThread.join(timeout=2)
