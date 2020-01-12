from gpiozero import LED

from models.Exceptions import InterfaceInitError
from models.Interface import Interface


class PureGPIO(Interface):

	def __init__(self, numLeds, pinout, activeHigh):
		super(PureGPIO, self).__init__(numLeds)

		if len(pinout) != numLeds:
			raise InterfaceInitError('Pure GPIO number of led versus pinout declaration missmatch')

		self._pinout 		= pinout
		self._activeHigh 	= activeHigh
		self._image 		= self._newArray()

		self._leds 		= []
		for pin in self._pinout:
			self._leds.append(LED(pin=pin, active_high=activeHigh, initial_value=False))


	def setPixel(self, ledNum, red, green, blue, brightness):
		"""
		Set pixel here doesn't take RGB(W) values but sets the led on/off instead
		:param red: int
		:param green: int
		:param blue: int
		:param brightness: int
		:type ledNum: int
		"""

		if ledNum < 0 or ledNum >= self._numLeds:
			self._logger.warning('Trying to access a led index out of reach')
			return

		if red > 0 or green > 0 or blue > 0 or brightness > 0:
			self._image[ledNum] = 1
		else:
			self._image[ledNum] = 0


	def setPixelRgb(self, ledNum, color, brightness):
		self.setPixel(ledNum, color[0], color[1], color[2], brightness)


	def clearStrip(self):
		self._image = self._newArray()
		self.show()


	def show(self):
		for index, status in enumerate(self._image):
			if status <= 0:
				self._leds[index].off()
			else:
				self._leds[index].on()


	def onStop(self):
		for led in self._leds:
			led.off()

	def _newArray(self):
		return [0] * self._numLeds
