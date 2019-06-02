from tkinter import *
from host.MCHandle import *
from host.MCHandleTrainer import *
import multiprocessing


def handle():
    _handle = MCHandle()
    _handle.mainloop()


def trainer():
    _trainer = MCHandleTrainer()
    _trainer.mainloop()


def start_handle():
    root.destroy()
    p = multiprocessing.Process(target=handle)
    p.start()


def start_trainer():
    root.destroy()
    p = multiprocessing.Process(target=trainer)
    p.start()


if __name__ == '__main__':
    root = Tk()
    multiprocessing.freeze_support()
    Button(root, text='训练器', command=start_trainer).pack()
    Button(root, text='手柄主程序', command=start_handle).pack()
    root.mainloop()
