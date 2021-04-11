import logging
from typing import Optional
import json


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

		configs = dict()
		try:
			#params.pathToConfig or
			with open('/home/pi/ProjectAlice/config.json') as jsonContent:
				conf = json.load(jsonContent)
				configs['mqttServer'] = conf['mqttHost']
				configs['mqttPort'] = conf['mqttPort']
				configs['mqttUsername'] = conf['mqttUser']
				configs['mqttPassword'] = conf['mqttPassword']
				configs['mqttTLSCAFile'] = conf['mqttTLSFile']

				configs['deviceName'] = conf['uuid']

			return configs
		except Exception as e:
			self._logger.info('Error loading configurations: {}'.format(e))
			return None
