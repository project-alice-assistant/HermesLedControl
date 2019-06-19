# -*- coding: utf-8 -*-

try:
	from gpiozero 			import LED
except:
	try:
		import mraa
	except:
		pass


from libraries.apa102   import APA102       as AAPA102
from models.Interface 	import Interface

class APA102(Interface):

	def __init__(self, numLed, global_brightness=AAPA102.MAX_BRIGHTNESS, order='rgb', bus=0, device=1, max_speed_hz=8000000, endFrame=255):
		super(APA102, self).__init__(numLed)
		self._leds  = AAPA102(numLed, global_brightness=global_brightness, order=order, bus=bus, device=device, max_speed_hz=max_speed_hz, endFrame=endFrame)

		try:
			self._power = LED(5)
		except:
			try:
				self._power = mraa.Gpio(12)
				self._power.dir(mraa.DIR_OUT)
			except:
				self._logger.info('Device not using gpiozero or mraa, ignore power')


	def setPixel(self, ledNum, red, green, blue, brightness):
		self._leds.set_pixel(ledNum, red, green, blue, brightness)


	def setPixelRgb(self, ledNum, color, brightness):
		self._leds.set_pixel_rgb(ledNum, color, brightness)


	def clearStrip(self):
		self._leds.clear_strip()


	def onStop(self):
		super(APA102, self).onStop()
		self.clearStrip()
		self._leds.cleanup()
