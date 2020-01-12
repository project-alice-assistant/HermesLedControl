import math

from libraries.neopixel import *
from models.Exceptions import InterfaceInitError
from models.Interface import Interface

try:
	import rpi_ws281x 	as ws
except ImportError:
	import _rpi_ws281x 	as ws

class Neopixels(Interface):

	_STRIP_TYPES = {
		'SK6812_RGBW':			0x18100800,
		'SK6812_RBGW':			0x18100008,
		'SK6812_GRBW':			0x18081000,
		'SK6812_GBRW':			0x18080010,
		'SK6812_BRGW':			0x18001008,
		'SK6812_BGRW':			0x18000810,
		'SK6812_SHIFT_WMASK':	0xf0000000,
		'WS2811_RGB':			0x00100800,
		'WS2811_RBG':			0x00100008,
		'WS2811_GRB':			0x00081000,
		'WS2811_GBR':			0x00080010,
		'WS2811_BRG':			0x00001008,
		'WS2811_BGR':			0x00000810,
		'WS2812':				0x00081000,
		'SK6812':				0x00081000,
		'SK6812W':				0x18081000
	}

	def __init__(self, numLeds, stripType, pin):
		super(Neopixels, self).__init__(numLeds)

		if stripType not in self._STRIP_TYPES:
			raise InterfaceInitError('Unsupported neopixel type "{}"'.format(stripType))

		self._type 	= stripType
		self._pin 	= pin
		self._leds 	= Adafruit_NeoPixel(num=numLeds, pin=pin, brightness=255, strip_type=self._STRIP_TYPES[stripType])
		self._leds.begin()


	def setPixel(self, ledNum, red, green, blue, brightness):
		if not str(self._type).endswith('W'):
			bRatio = float(brightness) / 255
			red = int(math.ceil(red * bRatio))
			green = int(math.ceil(green * bRatio))
			blue = int(math.ceil(blue * bRatio))
		self._leds.setPixelColorRGB(ledNum, red, green, blue, brightness)


	def setPixelRgb(self, ledNum, color, brightness=None):
		if not str(self._type).endswith('W') and brightness is not None:
			bRatio = float(brightness) / 255
			color[0] = int(math.ceil(color[0] * bRatio))
			color[1] = int(math.ceil(color[1] * bRatio))
			color[2] = int(math.ceil(color[2] * bRatio))
		self._leds.setPixelColor(ledNum, color)


	def clearStrip(self):
		for i in range(self._numLeds):
			self.setPixel(i, 0, 0, 0, 0)

		self.show()
