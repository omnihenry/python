from tkinter import *
from ssh_console import *


class SshWindow:

    def __init__(self, master):
        self.master = master
        master.title("Remote Command Exececuter")

        marginLeft  = 20
        marginRight = 20
        marginTop   = 20

        # Select host Label
        self.labelSelHost = Label(master, text="Please select remote host:")
        self.labelSelHost.grid(row=1, columnspan=3, sticky=W, padx=(marginLeft, 0), pady=(marginTop, 10))

        # Remote host list
        self.scrollbarHosts = Scrollbar(master, orient=VERTICAL)
        self.scrollbarHosts.grid(row=2, column=2, padx=(0, marginRight), sticky=NS)
        self.listBoxHosts = Listbox(master, width=50, height=5, yscrollcommand=self.scrollbarHosts.set)
        idx = 0
        for host in [conn[0] for conn in connectionList]:
            idx += 1             
            self.listBoxHosts.insert(idx, host)           
        self.listBoxHosts.grid(row=2, columnspan=2, padx=(marginLeft, 0))
        self.scrollbarHosts.config(command=self.listBoxHosts.yview)

        # Connect button
        self.btnConnect = Button(master, text='Connect', state=NORMAL, command=self.connectHost)
        self.btnConnect.grid(row=3, column=0, padx=(marginLeft, 0), sticky=W)

        # Disconnect button
        self.btnDisconnect = Button(master, text='Disconnect', state=DISABLED, command=self.disconnectHost)
        self.btnDisconnect.grid(row=3, column=1, sticky=E)

        # Message from connection
        self.resultConnect = StringVar()
        self.msgConnect = Message(master, textvariable=self.resultConnect, aspect=500)
        self.msgConnect.grid(row=5, column=0, columnspan=2, padx=(marginLeft, 0), sticky=N+S+E+W)

        # Select command label
        self.labelSelCmd = Label(master, text='Please select a command:')
        self.labelSelCmd.grid(row=10, columnspan=3, sticky=W, padx=(marginLeft, 0), pady=10)

        # Command list
        self.scrollbarCmds = Scrollbar(master, orient=VERTICAL)
        self.scrollbarCmds.grid(row=11, column=2, padx=(0, marginRight), sticky=NS)
        self.listBoxCmds = Listbox(master, width=50, height=5, yscrollcommand=self.scrollbarCmds.set)
        idx = 0
        for cmd in commandList:
            idx += 1             
            self.listBoxCmds.insert(idx, cmd)           
        self.listBoxCmds.grid(row=11, columnspan=2, padx=(marginLeft, 0))
        self.scrollbarCmds.config(command=self.listBoxCmds.yview)

        # Execute command button
        self.btnExec = Button(master, text='Execute', state=DISABLED, command=self.executeCmd)
        self.btnExec.grid(row=12, column=0, padx=(marginLeft, 0), sticky=W)

        # Message from execution
        self.resultExec = StringVar()
        self.msgExec = Message(master, textvariable=self.resultExec, aspect=500)
        self.msgExec.grid(row=15, column=0, columnspan=2, padx=(marginLeft, 0), sticky=N+S+E+W)

        # Exit button
        self.btnExit = Button(master, text='Close', command=self.closeApp)
        self.btnExit.grid(row=20, sticky=E)


        frame1 = Frame(width=200, height=150).grid()


    def connectHost(self):
        if self.listBoxHosts.curselection():
            selectedIndex = self.listBoxHosts.curselection()[0]
            host = self.listBoxHosts.get(selectedIndex)

            # set widget state
            self.btnConnect.config(state = DISABLED)
            self.resultConnect.set('Trying to connect to {}'.format(host))

            # establish connection
            self.sshConn = SshHandler()
            (resSuccessful, resMessage) = self.sshConn.connect(host)

            if resSuccessful:
                self.msgConnect.config(foreground = 'green')
                self.btnDisconnect.config(state = NORMAL)
                self.btnExec.config(state = NORMAL)
            else:
                self.msgConnect.config(foreground = 'red')
                self.btnConnect.config(state = NORMAL)

            self.resultConnect.set(resMessage)


    def executeCmd(self):
        if self.listBoxCmds.curselection():
            selectedIndex = self.listBoxCmds.curselection()[0]
            (resSuccessful, resMessage) = self.sshConn.executeCmd(self.listBoxCmds.get(selectedIndex))
            
            if resSuccessful:
                self.msgExec.config(foreground = 'blue')
            else:
                self.msgExec.config(foreground = 'red')

            self.resultExec.set(resMessage)


    def disconnectSsh(self):
        if hasattr(self, 'sshConn'):
            self.sshConn.disconnect()       

    def disconnectHost(self):
        self.disconnectSsh()

        # reset widget state
        self.btnConnect.config(state = NORMAL)
        self.btnDisconnect.config(state = DISABLED)
        self.btnExec.config(state = DISABLED)
        self.resultConnect.set('')
            

    def closeApp(self):
        self.disconnectSsh()
        self.master.destroy()



if __name__ == '__main__':
    logger.info('--- Starting main ---')
    root = Tk()
    #root.geometry("400x400+0+0")
    ssh_window = SshWindow(root)
    root.mainloop()
