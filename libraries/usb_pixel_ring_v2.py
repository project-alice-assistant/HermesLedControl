# -*- coding: utf-8 -*-

import usb.core
import usb.util


class PixelRing:
	TIMEOUT = 8000

	def __init__(self, dev):
		self.dev = dev

	def trace(self):
		self.write(0)

	def mono(self, color):
		self.write(1, [(color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF, 0])

	def set_color(self, rgb=None, r=0, g=0, b=0):
		if rgb:
			self.mono(rgb)
		else:
			self.write(1, [r, g, b, 0])

	def off(self):
		self.mono(0)

	def listen(self, direction=None):
		self.write(2)

	wakeup = listen

	def speak(self):
		self.write(3)

	def think(self):
		self.write(4)

	wait = think

	def spin(self):
		self.write(5)

	def show(self, data):
		self.write(6, data)
		self.set_brightness(data[3])

	customize = show

	def set_brightness(self, brightness):
		self.write(0x20, [brightness])

	def set_color_palette(self, a, b):
		self.write(0x21,
				   [(a >> 16) & 0xFF, (a >> 8) & 0xFF, a & 0xFF, 0, (b >> 16) & 0xFF, (b >> 8) & 0xFF, b & 0xFF, 0])

	def set_vad_led(self, state):
		self.write(0x22, [state])

	def set_volume(self, volume):
		self.write(0x23, [volume])

	def change_pattern(self, pattern):
		if pattern == 'echo':
			self.write(0x24, [1])
		else:
			self.write(0x24, [0])

	def write(self, cmd, data=None):
		if data is None:
			data = [0]

		self.dev.ctrl_transfer(
			usb.util.CTRL_OUT | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE,
			0, cmd, 0x1C, data, self.TIMEOUT)

	@property
	def version(self):
		return self.dev.ctrl_transfer(
			usb.util.CTRL_IN | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE,
			0, 0x80 | 0x40, 0x1C, 24, self.TIMEOUT).tostring()

	def close(self):
		"""
		close the interface
		"""
		usb.util.dispose_resources(self.dev)


def find(vid=0x2886, pid=0x0018):
	dev = usb.core.find(idVendor=vid, idProduct=pid)
	if not dev:
		return None

	return PixelRing(dev)
