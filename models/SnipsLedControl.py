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

	_SUB_ON_HOTWORD 			= 'hermes/hotword/default/detected'
	_SUB_ON_SAY 				= 'hermes/tts/say'
	_SUB_ON_THINK 				= 'hermes/asr/textCaptured'
	_SUB_ON_LISTENING 			= 'hermes/asr/startListening'
	_SUB_ON_HOTWORD_TOGGLE_ON 	= 'hermes/hotword/toggleOn'

	def __init__(self, pattern='google', pixels=12):
		self._logger = logging.getLogger('SnipsLedControl')
		self._logger.info('Initializing SnipsLedControl')

		self._snipsConfigs 	= self.loadConfigs()

		self._mqttServer 	= 'localhost'
		self._me 			= 'default'
		self._port 			= 1883 # TODO dynamic port loading

		try:
			if 'snips-common' in self._snipsConfigs and 'mqtt' in self._snipsConfigs['snips-common']:
				self._mqttServer = self._snipsConfigs['snips-common']['mqtt'].replace(':1883', '')
		except:
			self._logger.info('- Falling back to default config for mqtt server')

		try:
			if 'snips-audio-server' in self._snipsConfigs and 'bind' in self._snipsConfigs['snips-audio-server']:
				self._me = self._snipsConfigs['snips-audio-server']['bind'].replace('@mqtt', '')
		except:
			self._logger.info('- Falling back to default config for client id')

		self._logger.info('- Mqtt server set to {}'.format(self._mqttServer))
		self._logger.info('- ClientId set to {}'.format(self._me))

		self._leds = Pixels(pattern='google', pixels=12)
		self._mqttClient = self.connectMqtt()
		self._leds.wakeup()
		threading.Timer(interval=5, function=self._leds.off).start()
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
		mqttClient = mqtt.Client()
		mqttClient.on_connect = self.onConnect
		mqttClient.on_message = self.onMessage
		mqttClient.connect(self._mqttServer, 1883)
		mqttClient.loop_start()
		return mqttClient


	def onConnect(self, client, userdata, flags, rc):
		self._mqttClient.subscribe(self._SUB_ON_HOTWORD)
		self._mqttClient.subscribe(self._SUB_ON_SAY)
		self._mqttClient.subscribe(self._SUB_ON_THINK)
		self._mqttClient.subscribe(self._SUB_ON_LISTENING)
		self._mqttClient.subscribe(self._SUB_ON_HOTWORD_TOGGLE_ON)


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
				self._leds.off()


	def onStop(self):
		self._mqttClient.disconnect()
		self._leds.off()