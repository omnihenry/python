import paramiko
import json
import logging
from logging.handlers import RotatingFileHandler
from configparser import SafeConfigParser



class SshHandler:
    def __init__(self):

        config = SafeConfigParser()
        config.read('config.ini')

        # load configurations
        self.connectionList = json.loads(config.get('Remote Hosts', 'connection_list'))
        self.connectionAttemptMax = int(config.get('Connection', 'connect_attempt_max'))
        self.commandList = json.loads(config.get('Remote Actions', 'command_list'))
        logFile = config.get('Logging', 'log_file')
        logLevel = config.get('Logging', 'log_level')
        logSizeMax = int(config.get('Logging', 'log_size_max'))
        logRotateMax = int(config.get('Logging', 'log_rotate_max'))

        # init logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logLevel.upper())
        logHandler = RotatingFileHandler(logFile, maxBytes=logSizeMax, backupCount=logRotateMax)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logHandler.setFormatter(formatter)
        self.logger.addHandler(logHandler)


    def connect(self, remote):
        for host, username, password in [conn for conn in self.connectionList]:
            if host == remote:
                break;

        for i in range(self.connectionAttemptMax):
            try:
                self.logger.info('Connecting: %s - attempt #%d', host, i+1)
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, username=username, password=password)
                break

            except paramiko.AuthenticationException:
                print('Error: Authentication failed.')
                self.logger.error('Error: Authentication failed.')
                exit(1)

            except Exception as e:
                print('Error: Could not connect to ', host)
                self.logger.error('Error: Could not connect to %s', host)

        logging.shutdown()
        print('successful')


'''
# ------ from UI
selectedConn = 1
selectedComm = 0


host, username, password = connectionList[selectedConn]
command = commandList[selectedComm]

print(host, username, password)
print(command)
'''

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

