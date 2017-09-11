#!/usr/bin/python
# title           :ssh_gui.py
# description     :This script contains the class definition for UI
# author          :Hongbo Wang
# date            :20170820
# version         :0.1
# usage           :to be imported
# notes           :
# python_version  :3.6.2  
#==============================================================================

from tkinter import *
from ssh_handler import *

class SSHWindow:
    '''Show main window and handle operations.'''

    def __init__(self, master):
        '''
        Initialize widgets.

        :param master: parent widget
        '''
        self.master = master
        master.title("Remote Command Exececuter")

        # Select host Label
        self.label_sel_host = Label(master, text="Please select remote host:")
        self.label_sel_host.grid(row=1, column=0, columnspan=3, sticky=W, padx=(WINDOW_MARGIN_LEFT, 0), pady=(WINDOW_MARGIN_TOP, 10))

        # Remote host list
        self.scrollbar_hosts = Scrollbar(master, orient=VERTICAL)
        self.scrollbar_hosts.grid(row=2, column=2, padx=(0, WINDOW_MARGIN_RIGHT), sticky=NS)
        self.listbox_hosts = Listbox(master, width=70, height=5, yscrollcommand=self.scrollbar_hosts.set)
        idx = 0
        for host in [conn[0] for conn in CONNECTION_LIST]:
            idx += 1             
            self.listbox_hosts.insert(idx, host)           
        self.listbox_hosts.grid(row=2, column=0, columnspan=2, padx=(WINDOW_MARGIN_LEFT, 0), sticky=N+S+E+W)
        self.scrollbar_hosts.config(command=self.listbox_hosts.yview)

        # Connect button
        self.btn_connect = Button(master, text='Connect', state=NORMAL, command=self.connect_host)
        self.btn_connect.grid(row=3, column=0, padx=(WINDOW_MARGIN_LEFT, 0), sticky=W)

        # Disconnect button
        self.btn_disconnect = Button(master, text='Disconnect', state=DISABLED, command=self.disconnect_host)
        self.btn_disconnect.grid(row=3, column=1, sticky=E)

        # Message from connection
        self.result_connect = StringVar()
        self.msg_connect = Message(master, textvariable=self.result_connect, aspect=500)
        self.msg_connect.grid(row=5, column=0, columnspan=2, padx=(WINDOW_MARGIN_LEFT, 0), sticky=N+S+E+W)

        # Select command label
        self.label_sel_cmd = Label(master, text='Please select a command:')
        self.label_sel_cmd.grid(row=10, column=0, columnspan=3, sticky=W, padx=(WINDOW_MARGIN_LEFT, 0), pady=10)

        # Command list
        self.scrollbar_cmds = Scrollbar(master, orient=VERTICAL)
        self.scrollbar_cmds.grid(row=11, column=2, padx=(0, WINDOW_MARGIN_RIGHT), sticky=NS)
        self.listbox_cmds = Listbox(master, width=70, height=5, yscrollcommand=self.scrollbar_cmds.set)
        idx = 0
        for cmd in COMMAND_LIST:
            idx += 1             
            self.listbox_cmds.insert(idx, cmd)           
        self.listbox_cmds.grid(row=11, columnspan=2, padx=(WINDOW_MARGIN_LEFT, 0), sticky=N+S+E+W)
        self.scrollbar_cmds.config(command=self.listbox_cmds.yview)

        # Execute command button
        self.btn_exec = Button(master, text='Execute', state=DISABLED, command=self.execute_cmd)
        self.btn_exec.grid(row=12, column=0, padx=(WINDOW_MARGIN_LEFT, 0), pady=(0, WINDOW_MARGIN_BOTTOM), sticky=W)

        # Message from execution
        self.scrollbar_res = Scrollbar(master, orient=VERTICAL)
        self.scrollbar_res.grid(row=15, column=2, padx=(0, WINDOW_MARGIN_RIGHT), sticky=NS)
        self.msg_exec = Text(master, width=70, height=10, bg='black', borderwidth=3, relief=SUNKEN, yscrollcommand=self.scrollbar_res.set)
        self.msg_exec.grid(row=15, column=0, columnspan=2, padx=(WINDOW_MARGIN_LEFT, 0), sticky=N+S+E+W)
        self.scrollbar_res.config(command=self.msg_exec.yview)

        # Exit button
        self.btn_exit = Button(master, width=10, height=1, text='Close', command=self.close_app)
        self.btn_exit.grid(row=20, column=1, sticky=E, pady=(WINDOW_MARGIN_TOP, WINDOW_MARGIN_BOTTOM))

        logger.info('Main SSH Window initialized.')
        

    def connect_host(self):
        '''Establish connection to selected host.'''
        if self.listbox_hosts.curselection():
            selected_index = self.listbox_hosts.curselection()[0]
            host = self.listbox_hosts.get(selected_index)

            # Set widget state
            self.btn_connect.config(state = DISABLED)
            self.result_connect.set('Trying to connect to {}'.format(host))

            # Establish connection
            self.ssh_conn = SSHHandler()
            (res_successful, res_message) = self.ssh_conn.connect(host)

            # Reset state of widgets according to the result
            if res_successful:
                self.msg_connect.config(foreground = 'lime green')
                self.btn_disconnect.config(state = NORMAL)
                self.btn_exec.config(state = NORMAL)
            else:
                self.msg_connect.config(foreground = 'red')
                self.btn_connect.config(state = NORMAL)

            # Refresh the Message widget to show the connection result
            self.result_connect.set(res_message)


    def execute_cmd(self):
        '''Execute selected command on remote host.'''
        if self.listbox_cmds.curselection():
            selected_index = self.listbox_cmds.curselection()[0]
            (res_successful, res_message) = self.ssh_conn.execute_cmd(self.listbox_cmds.get(selected_index))
            
            # Reset the Message widget state according to the result
            if res_successful:
                self.msg_exec.config(foreground = 'white')
            else:
                self.msg_exec.config(foreground = 'red')

            # Refresh Text widget to show the result
            self.msg_exec.delete(1.0, END)
            self.msg_exec.insert(END, res_message)


    def disconnect_ssh(self):
        '''Disconnect remote host.'''
        if hasattr(self, 'ssh_conn'):
            self.ssh_conn.disconnect()     


    def disconnect_host(self):
        '''Disconnect remote host and reset widgets.'''
        self.disconnect_ssh()

        # reset widget state
        self.btn_connect.config(state = NORMAL)
        self.btn_disconnect.config(state = DISABLED)
        self.btn_exec.config(state = DISABLED)
        self.result_connect.set('')
            

    def close_app(self):
        '''Shutdown connection and close main window.'''
        self.disconnect_ssh()
        self.master.destroy()
        logger.info('Main SSH Window closed.')

