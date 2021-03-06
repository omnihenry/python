#!/usr/bin/python
# title           :ssh_globals.py
# description     :This module contains the definition of global variables
# author          :Hongbo Wang
# date            :20170820
# version         :0.1
# usage           :to be imported
# notes           :
# python_version  :3.6.2  
#==============================================================================

import json
import logging
from logging.handlers import RotatingFileHandler
from configparser import SafeConfigParser

# Load configuration file 
config = SafeConfigParser()
config.read('config.ini')

# Load configurations
CONNECTION_LIST = json.loads(config.get('Remote Hosts', 'CONNECTION_LIST'))
CONNECTION_ATTEMPT_MAX = int(config.get('Connection', 'CONNECT_ATTEMPT_MAX'))
COMMAND_LIST = json.loads(config.get('Remote Actions', 'COMMAND_LIST'))
LOG_FILE = config.get('Logging', 'LOG_FILE')
LOG_LEVEL = config.get('Logging', 'LOG_LEVEL')
LOG_SIZE_MAX = int(config.get('Logging', 'LOG_SIZE_MAX'))
LOG_ROTATE_MAX = int(config.get('Logging', 'LOG_ROTATE_MAX'))

WINDOW_MARGIN_TOP = config.get('User Interface', 'WINDOW_MARGIN_TOP')
WINDOW_MARGIN_BOTTOM = config.get('User Interface', 'WINDOW_MARGIN_BOTTOM')
WINDOW_MARGIN_LEFT = config.get('User Interface', 'WINDOW_MARGIN_LEFT')
WINDOW_MARGIN_RIGHT = config.get('User Interface', 'WINDOW_MARGIN_RIGHT')

# Initialize logging
logger = logging.getLogger('SSH App')
logger.setLevel(LOG_LEVEL.upper())
log_handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_SIZE_MAX, backupCount=LOG_ROTATE_MAX)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)