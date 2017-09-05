from tkinter import *
from ssh_console import *


class SshWindow:

    def __init__(self, master):
        self.master = master
        master.title("Remote Command Exececuter")

        # Top Label
        self.label = Label(master, text="Please select remote host:")
        self.label.grid(row=1, columnspan=2)

        # Remote host list
        self.scrollbarHosts = Scrollbar(master, orient=VERTICAL)
        self.scrollbarHosts.grid(row=2, column=2, sticky=NS)
        self.listBoxHosts = Listbox(master, width=30, height=5, yscrollcommand=self.scrollbarHosts.set)
        idx = 0
        for host in [conn[0] for conn in connectionList]:
            idx += 1             
            self.listBoxHosts.insert(idx, host)           
        self.listBoxHosts.grid(row=2, columnspan=2)
        self.scrollbarHosts.config(command=self.listBoxHosts.yview)

        # Connect button
        self.btnConnect = Button(master, text='Connect', state=NORMAL, command=self.connectHost)
        self.btnConnect.grid(row=3, column=0)

        # Disconnect button
        self.btnDisconnect = Button(master, text='Disconnect', state=DISABLED, command=self.disconnectHost)
        self.btnDisconnect.grid(row=3, column=1)

        # Message from connection
        self.resultConnect = StringVar()
        self.msgConnect = Message(master, textvariable=self.resultConnect, width=100)
        self.msgConnect.grid(row=4, columnspan=2, sticky=W)


        # Exit button
        self.btnExit = Button(master, text='Close', command=self.closeApp)
        self.btnExit.grid(row=5, sticky=E)


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
            self.resultConnect.set(resMessage)

            self.btnDisconnect.config(state = NORMAL)

    def disconnectSsh(self):
        if hasattr(self, 'sshConn'):
            self.sshConn.disconnect()       

    def disconnectHost(self):
        self.disconnectSsh()

        # reset widget state
        self.btnConnect.config(state = NORMAL)
        self.btnDisconnect.config(state = DISABLED)
        self.resultConnect.set('')
            

    def closeApp(self):
        self.disconnectSsh()
        self.master.destroy()



if __name__ == '__main__':
    logger.info('--- Starting main ---')
    root = Tk()
    ssh_window = SshWindow(root)
    root.mainloop()
