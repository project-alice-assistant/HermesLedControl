import respeaker.usb_hid

from models.Exceptions import InterfaceInitError
from models.Interface import Interface


class respeaker7MicArray(Interface):

	def __init__(self, numLeds):
		super(respeaker7MicArray, self).__init__(numLeds)

		self._image = self._newArray()

		try:
			self._leds = respeaker.usb_hid.get()
			if self._leds is None:
				raise InterfaceInitError()
		except InterfaceInitError:
			self._logger.error("Couldn't init respeaker 7 mic array")

	def setPixel(self, ledNum, red, green, blue, brightness):
		if ledNum < 0 or ledNum >= self._numLeds:
			self._logger.warning('Trying to access a led index out of reach')
			return

		self._image[ledNum] = [ledNum, red, green, blue, brightness]


	def setVolume(self, volume):
		#self.write(0, [5, 0, 0, volume])
		pass

	def setPixelRgb(self, ledNum, color, brightness):
		self.setPixel(ledNum, color[0], color[1], color[2], brightness)

	def clearStrip(self):
		self._image = self._newArray()
		self.show()

	def show(self):
		pass

	def onStop(self):
		pass

	def _newArray(self):
		return [0] * self._numLeds
