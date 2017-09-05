from ssh_gui import *

if __name__ == '__main__':
    logger.info('--- Starting main ---')
    root = Tk()
    ssh_window = SSHWindow(root)
    root.mainloop()
