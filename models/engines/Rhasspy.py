import os
import json
import logging
from pathlib import Path
from typing import Optional

import toml


class Rhasspy:

	def __init__(self):
		self._logger = logging.getLogger('HermesLedControl')
		self._logger.info('Initializing Rhasspy settings')


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

		userHomePath = os.path.expanduser('~')
		configPath = userHomePath + '/.config/rhasspy/profiles/en/profile.json'
		path = Path(configPath) if not params.pathToConfig else Path(params.pathToConfig)

		configs = dict()

		if path.exists():
			with path.open() as confFile:
				conf = json.load(confFile)

				try:
					configs['mqttServer'] = conf['mqtt']['host']
					configs['mqttPort'] = conf['mqtt']['port'] if 'port' in conf['mqtt'] else 1883
					configs['mqttUsername'] = conf['mqtt']['username'] if 'username' in conf['mqtt'] else ''
					configs['mqttPassword'] = conf['mqtt']['password'] if 'password' in conf['mqtt'] else ''
					configs['mqttTLSCAFile'] = ''
					configs['deviceName'] = conf['mqtt']['site_id'] if 'site_id' in conf['mqtt'] else 'default'

					return configs
				except:
					self._logger.info('Error loading configurations')
					return None
		else:
			if params.debug:
				self._logger.info('No Rhasspy config found but debug mode, allow to continue')
				return dict()
			else:
				self._logger.fatal('Error loading configurations, file does not exist')
				return None
