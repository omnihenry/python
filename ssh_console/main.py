#!/usr/bin/python
# title           :main.py
# description     :This is the main script of the application
# author          :Hongbo Wang
# date            :20170820
# version         :0.1
# usage           :python3 main.py
# notes           :
# python_version  :3.6.2  
#==============================================================================

from ssh_gui import *

if __name__ == '__main__':
    logger.info('--- Starting main ---')    
    root = Tk()
    # Initialize the main window    
    ssh_window = SSHWindow(root)
    # Show the main window
    root.mainloop()
