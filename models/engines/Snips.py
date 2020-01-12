import logging
from pathlib import Path
from typing import Optional

import toml


class Snips:

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
		path = Path('/etc/snips.toml') if not params.pathToConfig else params.pathToConfig

		configs = dict()

		if path.exists():
			with path.open() as confFile:
				conf = toml.load(confFile)

				try:
					configs['mqttServer'], configs['mqttPort'] = conf['snips-common']['mqtt'].split(':')
					configs['mqttUsername'] = conf.get('snips-common', dict()).get('mqtt_username', '')
					configs['mqttPassword'] = conf.get('snips-common', dict()).get('mqtt_password', '')
					configs['mqttTLSCAFile'] = conf.get('snips-common', dict()).get('mqtt_tls_cafile', '')
					configs['deviceName'] = conf.get('snips-audio-server', dict()).get('bind', 'default').replace('@mqtt', '')

					return configs
				except:
					self._logger.info('Error loading configurations')
					return None
		else:
			if params.debug:
				self._logger.info('No Snips config found but debug mode, allow to continue')
				return dict()
			else:
				self._logger.fatal('Error loading configurations, file does not exist')
				return None
