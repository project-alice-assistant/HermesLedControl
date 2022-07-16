import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Optional


class ProjectAlice(object):

	def __init__(self):
		self._logger = logging.getLogger('HermesLedControl')
		self._logger.info('Initializing ProjectAlice settings')


	def loadConfig(self, params: argparse.Namespace) -> Optional[Dict]:

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

		userHomePath = Path.home()
		configPath = userHomePath / 'ProjectAlice/config.json'
		path = Path(params.pathToConfig or configPath)

		configs = dict()
		try:
			with path.open() as jsonContent:
				conf = json.load(jsonContent)
				configs['mqttServer'] = conf['mqttHost']
				configs['mqttPort'] = conf['mqttPort']
				configs['mqttUsername'] = conf['mqttUser']
				configs['mqttPassword'] = conf['mqttPassword']
				configs['mqttTLSCAFile'] = conf['mqttTLSFile']
				configs['deviceName'] = conf['uuid']

			return configs
		except Exception as e:
			self._logger.info(f'Error loading configurations: {e}')
			return None
