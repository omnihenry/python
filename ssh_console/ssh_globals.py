"""
This module contains the definition of global variables
"""

import json
import logging
from logging.handlers import RotatingFileHandler
from configparser import SafeConfigParser


config = SafeConfigParser()
config.read('config.ini')

# load configurations
CONNECTION_LIST = json.loads(config.get('Remote Hosts', 'CONNECTION_LIST'))
CONNECTION_ATTEMPT_MAX = int(config.get('Connection', 'CONNECT_ATTEMPT_MAX'))
COMMAND_LIST = json.loads(config.get('Remote Actions', 'COMMAND_LIST'))
LOG_FILE = config.get('Logging', 'LOG_FILE')
LOG_LEVEL = config.get('Logging', 'LOG_LEVEL')
LOG_SIZE_MAX = int(config.get('Logging', 'LOG_SIZE_MAX'))
LOG_ROTATE_MAX = int(config.get('Logging', 'LOG_ROTATE_MAX'))

WINDOW_MARGIN_TOP = config.get('User Interface', 'WINDOW_MARGIN_TOP')
WINDOW_MARGIN_LEFT = config.get('User Interface', 'WINDOW_MARGIN_LEFT')
WINDOW_MARGIN_RIGHT = config.get('User Interface', 'WINDOW_MARGIN_RIGHT')

# init logging
logger = logging.getLogger('SSH App')
logger.setLevel(LOG_LEVEL.upper())
log_handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_SIZE_MAX, backupCount=LOG_ROTATE_MAX)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)