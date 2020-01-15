import math
import time

from models.LedPattern import LedPattern


class GoogleHomeLedPattern(LedPattern):

	def __init__(self, controller):
		super(GoogleHomeLedPattern, self).__init__(controller)

		self._cardinalSteps 	= int(math.ceil(self._numLeds / 4.00))
		self._colors 			= {
			'blue'		: [0, 0, 255, self._controller.defaultBrightness],
			'red'		: [255, 0, 0, self._controller.defaultBrightness],
			'yellow'	: [255, 255, 0, self._controller.defaultBrightness],
			'green'		: [0, 255, 0, self._controller.defaultBrightness]
		}
		self._colorRefs 		= ('blue', 'red', 'yellow', 'green')
		self._image 			= []


	def _newImage(self):
		# Drawing the Google color scheme by default
		self._image = []
		j = 0
		for i in range(self._numLeds):
			if i % self._cardinalSteps == 0:
				self._image.append(self._colors[self._colorRefs[j]])
				j += 1
			else:
				self._image.append([0, 0, 0, 0])


	def _rotateImage(self, angle):
		angle = round(angle)
		if angle == 0:
			self._logger.error('Cannot rotate by {}'.format(angle))
			return

		degreesPerLed = 360 / self._numLeds
		steps = int(math.ceil(angle / degreesPerLed))

		if steps < 0:
			for _ in range(0, steps, -1):
				insertBack = self._image.pop(0)
				self._image.insert(len(self._image), insertBack)
		else:
			for _ in range(steps):
				insertBack = self._image.pop()
				self._image.insert(0, insertBack)


	def _displayImage(self):
		for i, led in enumerate(self._image):
			self._controller.setLedRGB(i, led)

		self._controller.show()


	def wakeup(self):
		self._newImage()
		self._rotateImage(-90)
		self._displayImage()

		time.sleep(0.05)

		degreesPerLed = 360 / self._numLeds
		steps = int(math.ceil(90 / degreesPerLed))
		for _ in range(steps):
			self._rotateImage(degreesPerLed)
			self._displayImage()
			time.sleep(0.02)

		time.sleep(0.5)


	def listen(self):
		self._newImage()
		direction = 1
		brightness = self._controller.defaultBrightness
		self._animation.set()
		while self._animation.isSet():
			brightness -= direction
			for i in range(self._numLeds):
				self._image[i][3] = brightness
			self._displayImage()

			if brightness <= 10 or brightness >= self._controller.defaultBrightness:
				direction *= -1

			time.sleep(0.005)


	def think(self):
		self._animation.set()
		brightness = self._image[0][3]
		while brightness > 0:
			brightness -= 1
			for i in range(self._numLeds):
				self._image[i][3] = brightness
			self._displayImage()
			time.sleep(0.002)

		while brightness < self._controller.defaultBrightness:
			brightness += 1
			for led in self._image:
				led[3] = brightness
			self._displayImage()
			time.sleep(0.002)

		degreesPerLed = 360 / self._numLeds

		angle = 0
		while self._animation.isSet():
			self._rotateImage(degreesPerLed)
			self._displayImage()
			angle += degreesPerLed

			if angle >= 360:
				angle = 0

			time.sleep(0.1)

		diff = 360 - angle
		steps = int(math.ceil(diff / degreesPerLed))

		for _ in range(steps):
			self._rotateImage(degreesPerLed)
			self._displayImage()
			time.sleep(0.02)

		self.off()


	def speak(self):
		self._newImage()
		direction = 1
		brightness = self._controller.defaultBrightness
		self._animation.set()
		while self._animation.isSet():
			brightness -= direction
			for i, led in enumerate(self._image):
				self._image[i][3] = brightness
			self._displayImage()

			if brightness <= 10 or brightness >= self._controller.defaultBrightness:
				direction *= -1

			time.sleep(0.003)


	def idle(self, *args):
		self.off()


	def onStart(self, *args):
		self._controller.wakeup()
		self._controller.idle()
