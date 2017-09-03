import paramiko
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
logFile      = config.get('Logging', 'log_file')
logLevel     = config.get('Logging', 'log_level')
logSizeMax   = int(config.get('Logging', 'log_size_max'))
logRotateMax = int(config.get('Logging', 'log_rotate_max'))

#logging.basicConfig(filename=logFile,level=logLevel.upper())

logger = logging.getLogger(__name__)
logger.setLevel(logLevel.upper())
logHandler = RotatingFileHandler(logFile, maxBytes=logSizeMax, backupCount=logRotateMax)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)




# ------ from UI
selectedConn = 1
selectedComm = 0


host, username, password = connectionList[selectedConn]
command = commandList[selectedComm]

print(host, username, password)
print(command)

'''
for i in range(connectionAttemptMax):
    try:
        logger.info('Connecting: %s - attempt #%d', host, i+1)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)
        break

    except paramiko.AuthenticationException:
        print('Error: Authentication failed.')
        logger.error('Error: Authentication failed.')
        exit(1)

    except Exception as e:
        print('Error: Could not connect to ', host)
        logger.error('Error: Could not connect to %s', host)


stdin, stdout, stderr = ssh.exec_command(command)

err = stderr.read()
if (err):
    print('-- error --', err)
else:
    for line in (stdout.readlines()):
        print(line)


# close connections, files
stdin.close()
stderr.close()
stdout.close()
ssh.close()
'''

