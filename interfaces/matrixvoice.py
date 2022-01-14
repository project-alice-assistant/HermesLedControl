from matrix_lite import led

from models.Interface import Interface


class MatrixVoice(Interface):

	def __init__(self, numLeds: int):
		super(MatrixVoice, self).__init__(numLeds)
		self._colors = self._newArray()


	def setPixel(self, ledNum, red, green, blue, brightness):
		if ledNum < 0 or ledNum >= led.length:
			self._logger.warning('Trying to access a led index out of reach')
			return

		self._colors[ledNum - 1] = (red, green, blue, brightness)


	def setPixelRgb(self, ledNum, color, brightness):
		self.setPixel(ledNum, color[0], color[1], color[2], brightness)


	def clearStrip(self):
		self._colors = self._newArray()
		led.set()


	def show(self):
		led.set(self._colors)


	@staticmethod
	def _newArray():
		return [(0, 0, 0, 0) for _ in range(led.length)]
