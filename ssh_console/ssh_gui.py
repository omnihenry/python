from tkinter import *
from ssh_console import *

class SSHWindow:

    def __init__(self, master):
        self.master = master
        master.title("Remote Command Exececuter")

        margin_left  = 20
        margin_right = 20
        margin_top   = 20

        # Select host Label
        self.label_sel_host = Label(master, text="Please select remote host:")
        self.label_sel_host.grid(row=1, columnspan=3, sticky=W, padx=(margin_left, 0), pady=(margin_top, 10))

        # Remote host list
        self.scrollbar_osts = Scrollbar(master, orient=VERTICAL)
        self.scrollbar_osts.grid(row=2, column=2, padx=(0, margin_right), sticky=NS)
        self.listbox_hosts = Listbox(master, width=50, height=5, yscrollcommand=self.scrollbar_osts.set)
        idx = 0
        for host in [conn[0] for conn in connection_list]:
            idx += 1             
            self.listbox_hosts.insert(idx, host)           
        self.listbox_hosts.grid(row=2, columnspan=2, padx=(margin_left, 0))
        self.scrollbar_osts.config(command=self.listbox_hosts.yview)

        # Connect button
        self.btn_connect = Button(master, text='Connect', state=NORMAL, command=self.connect_host)
        self.btn_connect.grid(row=3, column=0, padx=(margin_left, 0), sticky=W)

        # Disconnect button
        self.btn_disconnect = Button(master, text='Disconnect', state=DISABLED, command=self.disconnect_host)
        self.btn_disconnect.grid(row=3, column=1, sticky=E)

        # Message from connection
        self.result_connect = StringVar()
        self.msg_connect = Message(master, textvariable=self.result_connect, aspect=500)
        self.msg_connect.grid(row=5, column=0, columnspan=2, padx=(margin_left, 0), sticky=N+S+E+W)

        # Select command label
        self.label_sel_cmd = Label(master, text='Please select a command:')
        self.label_sel_cmd.grid(row=10, columnspan=3, sticky=W, padx=(margin_left, 0), pady=10)

        # Command list
        self.scrollbar_cmds = Scrollbar(master, orient=VERTICAL)
        self.scrollbar_cmds.grid(row=11, column=2, padx=(0, margin_right), sticky=NS)
        self.listbox_cmds = Listbox(master, width=50, height=5, yscrollcommand=self.scrollbar_cmds.set)
        idx = 0
        for cmd in command_list:
            idx += 1             
            self.listbox_cmds.insert(idx, cmd)           
        self.listbox_cmds.grid(row=11, columnspan=2, padx=(margin_left, 0))
        self.scrollbar_cmds.config(command=self.listbox_cmds.yview)

        # Execute command button
        self.btn_exec = Button(master, text='Execute', state=DISABLED, command=self.execute_cmd)
        self.btn_exec.grid(row=12, column=0, padx=(margin_left, 0), sticky=W)

        # Message from execution
        self.scrollbar_res = Scrollbar(master, orient=VERTICAL)
        self.scrollbar_res.grid(row=15, column=2, padx=(0, margin_right), sticky=NS)
        self.msg_exec = Text(master, width=50, height=10, bg='black', borderwidth=3, relief=SUNKEN, yscrollcommand=self.scrollbar_res.set)
        self.msg_exec.grid(row=15, column=0, columnspan=2, padx=(margin_left, 0), sticky=N+S+E+W)
        self.scrollbar_res.config(command=self.msg_exec.yview)

        # Exit button
        self.btn_exit = Button(master, text='Close', command=self.close_app)
        self.btn_exit.grid(row=20, sticky=E)


        frame1 = Frame(width=200, height=150).grid()


    def connect_host(self):
        if self.listbox_hosts.curselection():
            selected_index = self.listbox_hosts.curselection()[0]
            host = self.listbox_hosts.get(selected_index)

            # set widget state
            self.btn_connect.config(state = DISABLED)
            self.result_connect.set('Trying to connect to {}'.format(host))

            # establish connection
            self.ssh_conn = SSHHandler()
            (res_successful, res_message) = self.ssh_conn.connect(host)

            if res_successful:
                self.msg_connect.config(foreground = 'lime green')
                self.btn_disconnect.config(state = NORMAL)
                self.btn_exec.config(state = NORMAL)
            else:
                self.msg_connect.config(foreground = 'red')
                self.btn_connect.config(state = NORMAL)

            self.result_connect.set(res_message)


    def execute_cmd(self):
        if self.listbox_cmds.curselection():
            selected_index = self.listbox_cmds.curselection()[0]
            (res_successful, res_message) = self.ssh_conn.execute_cmd(self.listbox_cmds.get(selected_index))
            
            if res_successful:
                self.msg_exec.config(foreground = 'white')
            else:
                self.msg_exec.config(foreground = 'red')

            self.msg_exec.delete(1.0, END)
            self.msg_exec.insert(END, res_message)


    def disconnect_ssh(self):
        if hasattr(self, 'ssh_conn'):
            self.ssh_conn.disconnect()       

    def disconnect_host(self):
        self.disconnect_ssh()

        # reset widget state
        self.btn_connect.config(state = NORMAL)
        self.btn_disconnect.config(state = DISABLED)
        self.btn_exec.config(state = DISABLED)
        self.result_connect.set('')
            

    def close_app(self):
        self.disconnect_ssh()
        self.master.destroy()

