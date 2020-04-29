# -*- coding: utf-8 -*-
import importlib

from gpiozero import LED

from libraries import usb_pixel_ring_v2    as pixel_ring
from models.Exceptions import InterfaceInitError
from models.Interface import Interface


class RespeakerMicArrayV2(Interface):

	def __init__(self, hardware, vid, pid):
		self._hardware = hardware
		super(RespeakerMicArrayV2, self).__init__(self._hardware['numberOfLeds'])

		self._leds = pixel_ring.find(vid=int(vid, 16), pid=int(pid, 16))

		if self._leds is None:
			raise InterfaceInitError('Respeaker Mic Array V2 not found using pid={} and vid={}'.format(pid, vid))

		self._colors = self._newArray()

		self._src = None
		if 'doa' in hardware and hardware['doa']:
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


	def onStart(self):
		super().onStart()
		if self._doa:
			self._logger.info('Starting DOA')
			self._src.recursive_start()


	def onStop(self):
		super().onStop()
		self.clearStrip()
		self._leds.close()
		if self._src:
			self._src.recursive_stop()


	def setPixel(self, ledNum, red, green, blue, brightness):
		if ledNum < 0 or ledNum >= self._numLeds:
			self._logger.warning('Trying to access a led index out of reach')
			return

		index = ledNum * 4
		self._colors[index] = red
		self._colors[index + 1] = green
		self._colors[index + 2] = blue
		self._colors[index + 3] = brightness


	def setPixelRgb(self, ledNum, color, brightness):
		self.setPixel(ledNum, color[0], color[1], color[2], brightness)


	def clearStrip(self):
		self._colors = self._newArray()
		self.show()


	def show(self):
		self._leds.customize(self._colors)


	def setVolume(self, volume):
		self._leds.set_volume(volume)


	def setVadLed(self, state):
		if state == 1:
			self._leds.set_vad_led(state)
		else:
			self._leds.set_vad_led(0)


	def _newArray(self):
		return [0, 0, 0, 0] * self._numLeds


	def doa(self):
		if self._doa:
			try:
				return self._doa.get_direction()
			except:
				pass

		return 0
