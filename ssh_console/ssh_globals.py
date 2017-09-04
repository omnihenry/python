
import json
import logging
from logging.handlers import RotatingFileHandler
from configparser import SafeConfigParser


config = SafeConfigParser()
config.read('config.ini')

# load configurations
connectionList = json.loads(config.get('Remote Hosts', 'connection_list'))
connectionAttemptMax = int(config.get('Connection', 'connect_attempt_max'))
commandList = json.loads(config.get('Remote Actions', 'command_list'))
logFile = config.get('Logging', 'log_file')
logLevel = config.get('Logging', 'log_level')
logSizeMax = int(config.get('Logging', 'log_size_max'))
logRotateMax = int(config.get('Logging', 'log_rotate_max'))

# init logging
logger = logging.getLogger('SSH App')
logger.setLevel(logLevel.upper())
logHandler = RotatingFileHandler(logFile, maxBytes=logSizeMax, backupCount=logRotateMax)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)