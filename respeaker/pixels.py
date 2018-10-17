import respeaker.apa102 		as apa102
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


class Pixels:
	INSTANCE = None

	def __init__(self, params):
		self._logger = logging.getLogger('SnipsLedControl')

		if self.INSTANCE is None:
			self.INSTANCE = self
		else:
			self._logger.error('Trying to instanciate Pixels but instance already exists')
			raise KeyboardInterrupt

		if params.pattern == 'google':
			self._pattern = GoogleHomeLedPattern(show=self.show)
		elif params.pattern == 'alexa':
			self._pattern = AlexaLedPattern(show=self.show)
		else:
			self._pattern = CustomLedPattern(show=self.show)

		self._dev = apa102.APA102(num_led=params.leds)

		self._pixels = params.leds
		self._power = LED(5)
		self._power.on()

		self._queue = Queue.Queue()
		self._thread = threading.Thread(target=self._run)
		self._thread.daemon = True
		self._thread.start()

		self._lastDirection = None


	def wakeup(self, direction=0):
		self._lastDirection = direction

		def f():
			self._pattern.wakeup(direction)

		self.put(f)


	def listen(self):
		if self._lastDirection:
			def f():
				self._pattern.wakeup(self._lastDirection)

			self.put(f)
		else:
			self.put(self._pattern.listen)


	def think(self):
		self.put(self._pattern.think)


	def speak(self):
		self.put(self._pattern.speak)


	def idle(self):
		self.put(self._pattern.idle)


	def off(self):
		self.put(self._pattern.off)


	def put(self, func):
		self._pattern.stop = True
		self._queue.put(func)


	def _run(self):
		while True:
			func = self._queue.get()
			self._pattern.stop = False
			func()


	def show(self, data):
		for i in range(self._pixels):
			self._dev.set_pixel(i, int(data[4 * i + 1]), int(data[4 * i + 2]), int(data[4 * i + 3]))

		self._dev.show()

