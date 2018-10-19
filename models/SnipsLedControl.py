#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import paho.mqtt.client as mqtt
from respeaker.pixels import Pixels
import pytoml
import threading

class SnipsLedControl:

	_SUB_ON_HOTWORD 				= 'hermes/hotword/default/detected'
	_SUB_ON_SAY 					= 'hermes/tts/say'
	_SUB_ON_THINK 					= 'hermes/asr/textCaptured'
	_SUB_ON_LISTENING 				= 'hermes/asr/startListening'
	_SUB_ON_HOTWORD_TOGGLE_ON 		= 'hermes/hotword/toggleOn'
	_SUB_ON_LEDS_TOGGLE 			= 'hermes/leds/toggle'
	_SUB_ON_LEDS_TOGGLE_ON 			= 'hermes/leds/toggleOn'
	_SUB_ON_LEDS_TOGGLE_OFF 		= 'hermes/leds/toggleOff'
	_SUB_ON_LEDS_ON_ERROR 			= 'hermes/nlu/intentNotRecognized'
	_SUB_ON_LEDS_ON_SUCCESS 		= 'hermes/nlu/intentParsed'


	def __init__(self, params):
		self._logger = logging.getLogger('SnipsLedControl')
		self._logger.info('Initializing SnipsLedControl')

		self._snipsConfigs 	= self.loadConfigs()

		self._params 				= params
		self._mqttServer 			= 'localhost'
		self._me 					= 'default'
		self._mqttPort 				= 1883
		self._hardwareReference 	= None

		with open('hardware.json') as f:
			self._hardwareReference = json.load(f)
			print('Loaded {} hardware references'.format(len(self._hardwareReference)))

		if params.mqttServer is None:
			try:
				if 'snips-common' in self._snipsConfigs and 'mqtt' in self._snipsConfigs['snips-common']:
					self._mqttServer = self._snipsConfigs['snips-common']['mqtt'].replace(':1883', '')
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

		if params.mqttPort is None:
			try:
				if 'snips-common' in self._snipsConfigs and 'mqtt' in self._snipsConfigs['snips-common']:
					port = self._snipsConfigs['snips-common']['mqtt'].split(':')[1]
			except:
				self._logger.info('- Falling back to default config for mqtt port')
		else:
			self._mqttPort = params.mqttPort

		self._logger.info('- Mqtt server set to {}'.format(self._mqttServer))
		self._logger.info('- Mqtt port set to {}'.format(self._mqttPort))
		self._logger.info('- Client id set to {}'.format(self._me))
		self._logger.info('- Using {} as pattern with {} leds'.format(params.pattern, params.leds))

		self._leds = Pixels(params)
		self._mqttClient = self.connectMqtt()
		self._leds.wakeup()

		threading.Timer(interval=5, function=self._leds.idle).start()
		self._logger.info('Snips Led Control started')


	def loadConfigs(self):
		self._logger.info('Loading configurations')

		if os.path.isfile('/etc/snips.toml'):
			with open('/etc/snips.toml') as confFile:
				configs = pytoml.load(confFile)
				return configs

		self._logger.error('Error loading configurations')
		self.onStop()
		return None


	def connectMqtt(self):
		try:
			mqttClient = mqtt.Client()
			mqttClient.on_connect = self.onConnect
			mqttClient.on_message = self.onMessage
			mqttClient.connect(self._mqttServer, self._mqttPort)
			mqttClient.loop_start()
			return mqttClient
		except:
			self._logger.error("Couldn't connect to mqtt, aborting")
			self.onStop()

	def onConnect(self, client, userdata, flags, rc):
		self._mqttClient.subscribe(self._SUB_ON_HOTWORD)
		self._mqttClient.subscribe(self._SUB_ON_SAY)
		self._mqttClient.subscribe(self._SUB_ON_THINK)
		self._mqttClient.subscribe(self._SUB_ON_LISTENING)
		self._mqttClient.subscribe(self._SUB_ON_HOTWORD_TOGGLE_ON)
		self._mqttClient.subscribe(self._SUB_ON_LEDS_TOGGLE_ON)
		self._mqttClient.subscribe(self._SUB_ON_LEDS_TOGGLE_OFF)
		self._mqttClient.subscribe(self._SUB_ON_LEDS_TOGGLE)
		self._mqttClient.subscribe(self._SUB_ON_LEDS_ON_ERROR)
		self._mqttClient.subscribe(self._SUB_ON_LEDS_ON_SUCCESS)


	def onMessage(self, client, userdata, message):
		payload = None

		if hasattr(message, 'payload') and message.payload != '':
			payload = json.loads(message.payload)

		if payload is not None and 'siteId' in payload:
			siteId = payload['siteId']
		else:
			siteId = None

		if message.topic == self._SUB_ON_HOTWORD:
			if siteId == self._me:
				self._leds.wakeup()
		elif message.topic == self._SUB_ON_LISTENING:
			if siteId == self._me:
				self._leds.listen()
		elif message.topic == self._SUB_ON_SAY:
			if siteId == self._me:
				self._leds.speak()
		elif message.topic == self._SUB_ON_THINK:
			if siteId == self._me:
				self._leds.think()
		elif message.topic == self._SUB_ON_HOTWORD_TOGGLE_ON:
			if siteId == self._me:
				self._leds.idle()
		elif message.topic == self._SUB_ON_LEDS_TOGGLE_ON:
			if siteId == self._me:
				self._leds.toggleStateOn()
		elif message.topic == self._SUB_ON_LEDS_TOGGLE_OFF:
			if siteId == self._me:
				self._leds.toggleStateOff()
		elif message.topic == self._SUB_ON_LEDS_TOGGLE:
			if siteId == self._me:
				self._leds.toggleState()
		elif message.topic == self._SUB_ON_LEDS_ON_SUCCESS:
			if siteId == self._me:
				self._leds.onSuccess()
		elif message.topic == self._SUB_ON_LEDS_ON_ERROR:
			if siteId == self._me:
				self._leds.onError()


	def onStop(self):
		self._mqttClient.disconnect()
		self._leds.onStop()