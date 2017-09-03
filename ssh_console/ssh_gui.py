from tkinter import Tk, Label, Listbox, Button, Message, TOP, LEFT, W, NORMAL, DISABLED, StringVar

from ssh_console import *
#import json
#from configparser import SafeConfigParser


config = SafeConfigParser()
config.read('config.ini')


class SshWindow:

    def __init__(self, master):
        self.master = master
        master.title("Remote Command Exececuter")

        self.label = Label(master, text="Please select remote host:")
        self.label.pack(side=TOP)

        # Remote host list
        self.listBoxHosts = Listbox(master)
        connectionList = json.loads(config.get('Remote Hosts', 'connection_list'))
        idx = 0
        for host in [conn[0] for conn in connectionList]:
            idx += 1             
            self.listBoxHosts.insert(idx, host)           
        self.listBoxHosts.pack()

        # Connect button
        self.btnConnect = Button(master, text='Connect', state=NORMAL, command=self.connectHost)
        self.btnConnect.pack()

        # Message from connection
        self.resultConnect = StringVar()
        self.msgConnect = Message(master, textvariable=self.resultConnect)
        self.msgConnect.pack()


    def connectHost(self):
        if self.listBoxHosts.curselection():
            selectedIndex = self.listBoxHosts.curselection()[0]
            host = self.listBoxHosts.get(selectedIndex)

            self.sshConn = SshHandler()
            self.sshConn.connect(host)
            del self.sshConn




if __name__ == '__main__':
    root = Tk()
    ssh_window = SshWindow(root)
    root.mainloop()