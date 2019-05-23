from tkinter import *


class MCHandle:

    def __init__(self, root=None):
        self.root = root
        if self.root is None:
            self.root = Tk()

    def mainloop(self):
        self.root.mainloop()


if __name__ == '__main__':
    _handle = MCHandle()
    _handle.mainloop()
