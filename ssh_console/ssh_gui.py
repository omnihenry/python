from Tkinter import Tk, Label, Listbox, Button, TOP, LEFT, W

import json
from configparser import SafeConfigParser


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
        self.btnConnect = Button(master, text='Connect', command=self.connectHost)
        self.btnConnect.pack()


    def connectHost(self):
        selectedIndex = self.listBoxHosts.curselection()[0]
        print(self.listBoxHosts.get(selectedIndex))




if __name__ == '__main__':
    root = Tk()
    ssh_window = SshWindow(root)
    root.mainloop()