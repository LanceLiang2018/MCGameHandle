from tkinter import *
from keras.layers import Dense
from keras.models import Sequential
import serial
import serial.tools.list_ports


class MCHandleTrainer:

    def __init__(self, root=None):
        self.root = root
        if self.root is None:
            self.root = Tk()
        self.port = ''
        self.bps = 115200
        self.serial = None

        self.init_port = StringVar()
        self.init_bps = IntVar()

    def init_communication(self):
        top = Toplevel(self.root)
        top.mainloop()

    def init_communication_ok(self):
        pass

    def mainloop(self):
        self.root.mainloop()


if __name__ == '__main__':
    _trainer = MCHandleTrainer()
    _trainer.mainloop()