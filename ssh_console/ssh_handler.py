#!/usr/bin/python
# title           :ssh_handler.py
# description     :This script contains the definition of the class 
#                  that encapsulate the functionalities of remote access
# author          :HB
# date            :20170820
# version         :0.1
# usage           :to be imported
# notes           :
# python_version  :3.6.2  
#==============================================================================

from ssh_globals import *
import paramiko


class SSHHandler:
    """Handle SSH connections and remote command executions."""

    def __init__(self):
        """Do nothing here."""
        pass


    def connect(self, remote):
        """
        Connect to remote host 
      
        :param remote: remote host ip
        """
        result_successful, result_message = True, ''

        for host, username, password in [conn for conn in CONNECTION_LIST]:
            if host == remote:
                break;

        # try to connect for pre-definded number of times
        for idx in range(CONNECTION_ATTEMPT_MAX):
            try:
                logger.info('Connecting to {} - attempt #{}'.format(host, idx+1))
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(host, username=username, password=password)

            except paramiko.AuthenticationException:
                result_message = 'Error: Authentication failed when connecting to {}'.format(host)
                logger.error(result_message)
                result_successful = False            

            except Exception as e:                         # Other exceptions
                result_message = 'Error: Could not connect to {} - {}'.format(host, e)
                logger.error(result_message)
                result_successful = False

            else:                                          # If it's all good   
                result_message = 'Successfully connected to {}'.format(host)
                logger.info(result_message)
                result_successful = True
                break

        return (result_successful, result_message)


    def execute_cmd(self, cmd):
        """Execute command on connected host."""
        logger.info('Executing command: {}'.format(cmd))
        result_successful, result_message = True, ''

        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
        except Exception as e:                  # All exceptions
            result_successful = False
            result_message = str(e)
        else:
            # If command was run, catch the result.
            err = stderr.read()
            if (err):
                result_successful = False
                result_message = err
                logger.info('Failed.')
            else:
                result_successful = True
                result_message = stdout.read()
                logger.info('Successful.')
        finally:
            # Release resources before leaving
            stdin.close()
            stderr.close()
            stdout.close()

        return (result_successful, result_message)


    def disconnect(self):
        """Disconnect from remote host."""
        if hasattr(self, 'ssh'):
            self.ssh.close()
        logger.info('Disconnected')


