from ssh_globals import *
import paramiko


class SshHandler:
    def __init__(self):
        pass

    def connect(self, remote):
        resultSuccessful = True
        resultMessage = ''

        for host, username, password in [conn for conn in connectionList]:
            if host == remote:
                break;

        for i in range(connectionAttemptMax):
            try:
                logger.info('Connecting to {} - attempt #{}'.format(host, i+1))
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(host, username=username, password=password)

            except paramiko.AuthenticationException:
                resultMessage = 'Error: Authentication failed when connecting to {}'.format(host)
                logger.error(resultMessage)
                resultSuccessful = False            

            except Exception as e:
                resultMessage = 'Error: Could not connect to {} - {}'.format(host, e)
                logger.error(resultMessage)
                resultSuccessful = False

            else:
                resultMessage = 'Successfully connected to {}'.format(host)
                logger.info(resultMessage)
                resultSuccessful = True
                break

        print(resultMessage)
        return (resultSuccessful, resultMessage)

    def executeCmd(self, cmd):
        resultSuccessful = True
        resultMessage = ''

        stdin, stdout, stderr = self.ssh.exec_command(cmd)

        err = stderr.read()
        if (err):
            resultSuccessful = False
            resultMessage = err
        else:
            resultSuccessful = True
            resultMessage = stdout.read()

        return (resultSuccessful, resultMessage)


    def disconnect(self):
        if hasattr(self, 'ssh'):
            self.ssh.close()
        print('Disconnected')
        logger.info('Disconnected')



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

