#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from models.LedsController import LedsController
import os
import paho.mqtt.client as mqtt
import pytoml
import sys

class SnipsLedControl:

	_SUB_ON_HOTWORD 				= 'hermes/hotword/default/detected'
	_SUB_ON_SAY 					= 'hermes/tts/say'
	_SUB_ON_THINK 					= 'hermes/asr/textCaptured'
	_SUB_ON_LISTENING 				= 'hermes/asr/startListening'
	_SUB_ON_HOTWORD_TOGGLE_ON 		= 'hermes/hotword/toggleOn'
	_SUB_LEDS_ON_ERROR 				= 'hermes/nlu/intentNotRecognized'
	_SUB_LEDS_ON_SUCCESS 			= 'hermes/nlu/intentParsed'
	_SUB_ON_PLAY_FINISHED 			= 'hermes/audioServer/{}/playFinished'
	_SUB_ON_TTS_FINISHED 			= 'hermes/tts/sayFinished'

	_SUB_ON_LEDS_TOGGLE 			= 'hermes/leds/toggle'
	_SUB_ON_LEDS_TOGGLE_ON 			= 'hermes/leds/toggleOn'
	_SUB_ON_LEDS_TOGGLE_OFF 		= 'hermes/leds/toggleOff'
	_SUB_UPDATING 					= 'hermes/leds/systemUpdate'
	_SUB_ON_CALL 					= 'hermes/leds/onCall'
	_SUB_SETUP_MODE 				= 'hermes/leds/setupMode'
	_SUB_CON_ERROR 					= 'hermes/leds/connectionError'
	_SUB_ON_MESSAGE 				= 'hermes/leds/onMessage'
	_SUB_ON_DND 					= 'hermes/leds/doNotDisturb'


	def __init__(self, params):
		self._logger = logging.getLogger('SnipsLedControl')
		self._logger.info('Initializing SnipsLedControl')

		self._mqttClient 			= None
		self._hardwareReference 	= None
		self._ledsController 		= None
		self._params 				= params

		self._snipsConfigs 	= self.loadConfigs()

		self._mqttServer 			= 'localhost'
		self._me 					= 'default'
		self._mqttPort 				= 1883
		self._mqttUsername 			= ''
		self._mqttPassword 			= ''

		with open('hardware.json') as f:
			self._hardwareReference = json.load(f)
			self._logger.info('Loaded {} hardware references'.format(len(self._hardwareReference)))

		if params.hardware not in self._hardwareReference:
			self._logger.fatal('Trying to use an unsupported hardware')
			self.onStop()
		else:
			self._hardware = self._hardwareReference[self._params.hardware]

		if params.mqttServer is None:
			try:
				if 'snips-common' in self._snipsConfigs and 'mqtt' in self._snipsConfigs['snips-common']:
					self._mqttServer = self._snipsConfigs['snips-common']['mqtt'].replace(':1883', '')

					if 'mqtt_username' in self._snipsConfigs['snips-common'] and params.mqttUsername is None:
						self._mqttUsername = self._snipsConfigs['snips-common']['mqtt_username']

					if 'mqtt_password' in self._snipsConfigs['snips-common'] and params.mqttPassword is None:
						self._mqttPassword = self._snipsConfigs['snips-common']['mqtt_password']

			except:
				self._logger.info('- Falling back to default config for mqtt server')
		else:
			self._mqttServer = params.mqttServer


		if params.clientId is None:
			try:
				if 'snips-audio-server' in self._snipsConfigs and 'bind' in self._snipsConfigs['snips-audio-server']:
					self._me = self._snipsConfigs['snips-audio-server']['bind'].replace('@mqtt', '')
			except:
				self._logger.info('- Falling back to default config for client id')
		else:
			self._me = params.clientId


		self._SUB_ON_PLAY_FINISHED = self._SUB_ON_PLAY_FINISHED.format(self._me)


		if params.mqttPort is None:
			try:
				if 'snips-common' in self._snipsConfigs and 'mqtt' in self._snipsConfigs['snips-common']:
					self._mqttPort = self._snipsConfigs['snips-common']['mqtt'].split(':')[1]
			except:
				self._logger.info('- Falling back to default config for mqtt port')
		else:
			self._mqttPort = params.mqttPort

		self._logger.info('- Mqtt server set to {}'.format(self._mqttServer))
		self._logger.info('- Mqtt port set to {}'.format(self._mqttPort))

		if self._mqttUsername:
			self._logger.info('- Mqtt username set to {}'.format(self._mqttUsername))
		if self._mqttPassword:
			self._logger.info('- Mqtt password set to "hidden"')

		self._logger.info('- Client id set to {}'.format(self._me))
		self._logger.info('- Hardware set to {}'.format(self._hardware['name']))

		string = '- Using {} as pattern with {} leds'
		if params.leds is not None:
			self._logger.info(string.format(params.pattern, params.leds))
			self._hardware['numberOfLeds'] = params.leds
		else:
			self._logger.info(string.format(params.pattern, self._hardware['numberOfLeds']))

		if 'gpioPin' in self._hardware:
			string = 'Using pin #{}'
			if params.gpioPin is not None:
				self._logger.info(string.format(params.gpioPin))
				self._hardware['gpioPin'] = params.gpioPin
			else:
				self._logger.info(string.format(self._hardware['gpioPin']))

		if 'vid' in self._hardware and params.vid is not None:
			self._hardware['vid'] = params.vid

		if 'gpios' in self._hardware and len(params.pureGpioPinout) > 0:
			self.hardware['gpios'] = params.pureGpioPinout

		if 'activeHigh' in self._hardware and params.activeHigh != self._hardware['activeHigh']:
			self._hardware['activeHigh'] = params.activeHigh

		if 'endFrame' in self._hardware and params.endFrame is not None:
			self._hardware['endFrame'] = params.endFrame


		self._ledsController = LedsController(self)
		self._mqttClient = self.connectMqtt()


	def onStart(self):
		self._ledsController.onStart()
		self._logger.info('Snips Led Control started')


	def onStop(self):
		if self._mqttClient is not None:
			self._mqttClient.disconnect()

		if self._ledsController is not None:
			self._ledsController.onStop()

		sys.exit(0)


	def loadConfigs(self):
		self._logger.info('Loading configurations')

		if os.path.isfile('/etc/snips.toml'):
			with open('/etc/snips.toml') as confFile:
				configs = pytoml.load(confFile)
				return configs
		else:
			if self.params.debug:
				self._logger.info('No snips config found but debug mode, allow to continue')
				return None
			else:
				self._logger.fatal('Error loading configurations')
				self.onStop()
				return None


	def connectMqtt(self):
		try:
			mqttClient = mqtt.Client()

			if self._mqttUsername and self._mqttPassword:
				mqttClient.username_pw_set(self._mqttUsername, self._mqttPassword)

			mqttClient.on_connect = self.onConnect
			mqttClient.on_message = self.onMessage
			mqttClient.connect(self._mqttServer, int(self._mqttPort))
			mqttClient.loop_start()
			return mqttClient
		except:
			self._logger.fatal("Couldn't connect to mqtt, aborting")
			self.onStop()


	def onConnect(self, client, userdata, flags, rc):
		self._mqttClient.subscribe([
			(self._SUB_ON_HOTWORD, 0),
			(self._SUB_ON_SAY, 0),
			(self._SUB_ON_THINK, 0),
			(self._SUB_ON_LISTENING, 0),
			(self._SUB_ON_LEDS_TOGGLE_ON, 0),
			(self._SUB_ON_LEDS_TOGGLE_OFF, 0),
			(self._SUB_ON_LEDS_TOGGLE, 0),
			(self._SUB_LEDS_ON_ERROR, 0),
			(self._SUB_LEDS_ON_SUCCESS, 0)
		])

		self._mqttClient.subscribe(self._params.offListener)


	def onMessage(self, client, userdata, message):
		payload = None

		if hasattr(message, 'payload') and message.payload:
			payload = json.loads(message.payload)

		if payload is not None and 'siteId' in payload:
			siteId = payload['siteId']
		else:
			siteId = None

		if message.topic == self._SUB_ON_HOTWORD:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On hotword triggered')
				self._ledsController.wakeup()
			else:
				if self._params.debug:
					self._logger.debug("On hotword received, but it wasn't for me")
		elif message.topic == self._SUB_ON_LISTENING:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On listen triggered')
				self._ledsController.listen()
			else:
				if self._params.debug:
					self._logger.debug("On listen received, but it wasn't for me")
		elif message.topic == self._SUB_ON_SAY:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On say triggered')
				self._ledsController.speak()
			else:
				if self._params.debug:
					self._logger.debug("On say received, but it wasn't for me")
		elif message.topic == self._SUB_ON_THINK:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On think triggered')
				self._ledsController.think()
			else:
				if self._params.debug:
					self._logger.debug("On think received, but it wasn't for me")
		elif message.topic == self._SUB_ON_HOTWORD_TOGGLE_ON:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On hotword toggle on triggered')
				self._ledsController.idle()
			else:
				if self._params.debug:
					self._logger.debug("On hotword toggle on received, but it wasn't for me")
		elif message.topic == self._SUB_ON_TTS_FINISHED:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On tts finished triggered')
				self._ledsController.idle()
			else:
				if self._params.debug:
					self._logger.debug("On tts finished received, but it wasn't for me")
		elif message.topic == self._SUB_ON_PLAY_FINISHED:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On play finished triggered')
				self._ledsController.idle()
			else:
				if self._params.debug:
					self._logger.debug("On play finished received, but it wasn't for me")
		elif message.topic == self._SUB_ON_LEDS_TOGGLE_ON:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On leds toggle on triggered')
				self._ledsController.toggleStateOn()
			else:
				if self._params.debug:
					self._logger.debug("On leds toggle on received, but it wasn't for me")
		elif message.topic == self._SUB_ON_LEDS_TOGGLE_OFF:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On leds toggle off triggered')
				self._ledsController.toggleStateOff()
			else:
				if self._params.debug:
					self._logger.debug("On leds toggle off received, but it wasn't for me")
		elif message.topic == self._SUB_ON_LEDS_TOGGLE:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On leds toggle triggered')
				self._ledsController.toggleState()
			else:
				if self._params.debug:
					self._logger.debug("On leds toggle received, but it wasn't for me")
		elif message.topic == self._SUB_LEDS_ON_SUCCESS:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On success triggered')
				self._ledsController.onSuccess()
			else:
				if self._params.debug:
					self._logger.debug("On success received, but it wasn't for me")
		elif message.topic == self._SUB_LEDS_ON_ERROR:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On error triggered')
				self._ledsController.onError()
			else:
				if self._params.debug:
					self._logger.debug("On error received, but it wasn't for me")
		elif message.topic == self._SUB_UPDATING:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On updating triggered')
				self._ledsController.updating()
			else:
				if self._params.debug:
					self._logger.debug("On updating received, but it wasn't for me")
		elif message.topic == self._SUB_ON_CALL:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On call triggered')
				self._ledsController.call()
			else:
				if self._params.debug:
					self._logger.debug("On call received, but it wasn't for me")
		elif message.topic == self._SUB_SETUP_MODE:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On setup mode triggered')
				self._ledsController.setupMode()
			else:
				if self._params.debug:
					self._logger.debug("On setup mode received, but it wasn't for me")
		elif message.topic == self._SUB_CON_ERROR:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On connection error triggered')
				self._ledsController.conError()
			else:
				if self._params.debug:
					self._logger.debug("On connection error received, but it wasn't for me")
		elif message.topic == self._SUB_ON_MESSAGE:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On message triggered')
				self._ledsController.message()
			else:
				if self._params.debug:
					self._logger.debug("On message received, but it wasn't for me")
		elif message.topic == self._SUB_ON_DND:
			if siteId == self._me:
				if self._params.debug:
					self._logger.debug('On do not disturb triggered')
				self._ledsController.dnd()
			else:
				if self._params.debug:
					self._logger.debug("On do not disturb received, but it wasn't for me")


	@property
	def params(self):
		return self._params


	@property
	def hardwareReference(self):
		return self._hardwareReference


	@property
	def hardware(self):
		return self._hardware