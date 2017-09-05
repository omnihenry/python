
import json
import logging
from logging.handlers import RotatingFileHandler
from configparser import SafeConfigParser


config = SafeConfigParser()
config.read('config.ini')

# load configurations
connection_list = json.loads(config.get('Remote Hosts', 'CONNECTION_LIST'))
connection_attempt_max = int(config.get('Connection', 'CONNECT_ATTEMPT_MAX'))
command_list = json.loads(config.get('Remote Actions', 'COMMAND_LIST'))
log_file = config.get('Logging', 'LOG_FILE')
log_level = config.get('Logging', 'LOG_LEVEL')
log_size_max = int(config.get('Logging', 'LOG_SIZE_MAX'))
log_rotate_max = int(config.get('Logging', 'LOG_ROTATE_MAX'))

# init logging
logger = logging.getLogger('SSH App')
logger.setLevel(log_level.upper())
log_handler = RotatingFileHandler(log_file, maxBytes=log_size_max, backupCount=log_rotate_max)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)