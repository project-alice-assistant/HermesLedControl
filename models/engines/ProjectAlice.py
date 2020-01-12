import logging
from pathlib import Path
from typing import Optional

import toml


class ProjectAlice:

	def __init__(self):
		self._logger = logging.getLogger('HermesLedControl')
		self._logger.info('Initializing ProjectAlice settings')


	def loadConfig(self, params) -> Optional[dict]:

		"""
		Load assistant configuration
		:return: configs are returned as a dict:
		{
		  'mqttServer': ip
		  'mqttPort': port
		  'mqttUsername': username, optional
		  'mqttPassword': password, optional
		  'mqttTLSCAFile': path to cacert TLS file, optional
		  'deviceName': name
		}
		"""

		self._logger.info('Loading configurations')
		path = params.pathToConfig or Path('/etc/snips.toml')

		configs = dict()

		if path.exists():
			with path.open() as confFile:
				conf = toml.load(confFile)

				try:
					snipsCommons = conf['snips-common']
					configs['mqttServer'], configs['mqttPort'] = snipsCommons['mqtt'].split(':')
					configs['mqttUsername'] = snipsCommons.get('mqtt_username', '')
					configs['mqttPassword'] = snipsCommons.get('mqtt_password', '')
					configs['mqttTLSCAFile'] = snipsCommons.get('mqtt_tls_cafile', '')

					snipsAudioServer = conf.get('snips-audio-server', dict())
					configs['deviceName'] = snipsAudioServer.get('bind', 'default').replace('@mqtt', '')

					return configs
				except:
					self._logger.info('Error loading configurations')
					return None
		else:
			if params.debug:
				self._logger.info('No Project Alice config found but debug mode, allow to continue')
				return dict()
			else:
				self._logger.fatal('Error loading configurations, file does not exist')
				return None
