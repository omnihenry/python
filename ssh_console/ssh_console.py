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

        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
        except Exception as e:
            resultSuccessful = False
            resultMessage = str(e)
        else:
            err = stderr.read()
            if (err):
                resultSuccessful = False
                resultMessage = err
            else:
                resultSuccessful = True
                resultMessage = stdout.read()
        finally:
            stdin.close()
            stderr.close()
            stdout.close()

        return (resultSuccessful, resultMessage)


    def disconnect(self):
        if hasattr(self, 'ssh'):
            self.ssh.close()
        print('Disconnected')
        logger.info('Disconnected')


