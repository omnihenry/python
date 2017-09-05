from ssh_globals import *
import paramiko


class SSHHandler:
    def __init__(self):
        pass

    def connect(self, remote):
        result_successful = True
        result_message = ''

        for host, username, password in [conn for conn in connection_list]:
            if host == remote:
                break;

        for i in range(connection_attempt_max):
            try:
                logger.info('Connecting to {} - attempt #{}'.format(host, i+1))
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(host, username=username, password=password)

            except paramiko.AuthenticationException:
                result_message = 'Error: Authentication failed when connecting to {}'.format(host)
                logger.error(result_message)
                result_successful = False            

            except Exception as e:
                result_message = 'Error: Could not connect to {} - {}'.format(host, e)
                logger.error(result_message)
                result_successful = False

            else:
                result_message = 'Successfully connected to {}'.format(host)
                logger.info(result_message)
                result_successful = True
                break

        print(result_message)
        return (result_successful, result_message)

    def execute_cmd(self, cmd):
        result_successful = True
        result_message = ''

        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
        except Exception as e:
            result_successful = False
            result_message = str(e)
        else:
            err = stderr.read()
            if (err):
                result_successful = False
                result_message = err
            else:
                result_successful = True
                result_message = stdout.read()
        finally:
            stdin.close()
            stderr.close()
            stdout.close()

        return (result_successful, result_message)


    def disconnect(self):
        if hasattr(self, 'ssh'):
            self.ssh.close()
        print('Disconnected')
        logger.info('Disconnected')


