import importlib
from typing import Dict, List

try:
	from gpiozero import LED
except:
	try:
		import mraa
	except:
		pass

from libraries.apa102 import APA102 as AAPA102
from models.Interface import Interface


class APA102(Interface):

	def __init__(self, hardware: Dict, global_brightness: int = AAPA102.MAX_BRIGHTNESS, order: str = 'rgb', bus: int = 0, device: int = 1, max_speed_hz: int = 8000000, endFrame: int = 255):
		super(APA102, self).__init__(hardware['numberOfLeds'])
		self._leds = AAPA102(hardware['numberOfLeds'], global_brightness=global_brightness, order=order, bus=bus, device=device, max_speed_hz=max_speed_hz, endFrame=endFrame)

		try:
			self._power = LED(5)
		except:
			try:
				self._power = mraa.Gpio(5)
				self._power.dir(mraa.DIR_OUT)
			except Exception as e:
				self._logger.info(f'Device not using gpiozero or mraa, ignore power: {e}')

		self._hardware = hardware
		self._src = None
		if hardware.get('doa'):
			self._logger.info('Hardware is DOA capable')
			from libraries.seeedstudios.channel_picker import ChannelPicker
			from libraries.seeedstudios.source import Source

			lib = importlib.import_module('libraries.seeedstudios.' + hardware['doa'])
			klass = getattr(lib, 'DOA')

			self._src = Source(rate=hardware['rate'], channels=hardware['channels'])
			ch0 = ChannelPicker(channels=self._src.channels, pick=0)

			self._doa = klass(rate=hardware['rate'])
			self._src.link(ch0)
			self._src.link(self._doa)


	def setPixel(self, ledNum: int, red: int, green: int, blue: int, brightness: int):
		self._leds.set_pixel(ledNum, red, green, blue, brightness)


	def setPixelRgb(self, ledNum: int, color: List, brightness: int):
		self._leds.set_pixel_rgb(ledNum, color, brightness)


	def clearStrip(self):
		self._leds.clear_strip()


	def onStart(self):
		super().onStart()
		if self._doa:
			self._logger.info('Starting DOA')
			self._src.recursive_start()


	def onStop(self):
		super().onStop()
		self.clearStrip()
		self._leds.cleanup()
		if self._src:
			self._src.recursive_stop()


	def doa(self) -> int:
		if self._doa:
			try:
				return self._doa.get_direction()
			except:
				return 0

		return 0
