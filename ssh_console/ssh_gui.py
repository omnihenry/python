from tkinter import Tk, Label, Listbox, Button, Message, TOP, LEFT, W, NORMAL, DISABLED, StringVar
import sys
import time
from ssh_console import *


class SshWindow:

    def __init__(self, master):
        self.master = master
        master.title("Remote Command Exececuter")

        self.label = Label(master, text="Please select remote host:")
        self.label.pack(side=TOP)

        # Remote host list
        self.listBoxHosts = Listbox(master)

        idx = 0
        for host in [conn[0] for conn in connectionList]:
            idx += 1             
            self.listBoxHosts.insert(idx, host)           
        self.listBoxHosts.pack()

        # Connect button
        self.btnConnect = Button(master, text='Connect', state=NORMAL, command=self.connectHost)
        self.btnConnect.pack()

        # Disconnect button
        self.btnDisconnect = Button(master, text='Disconnect', state=DISABLED, command=self.disconnectHost)
        self.btnDisconnect.pack()

        # Message from connection
        self.resultConnect = StringVar()
        self.msgConnect = Message(master, textvariable=self.resultConnect)
        self.msgConnect.pack()


        # Exit button
        self.btnExit = Button(master, text='Close', command=self.closeApp)
        self.btnExit.pack()


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
