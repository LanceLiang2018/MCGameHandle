from tkinter import *
from tkinter import messagebox
# from keras.layers import Dense
# from keras.models import Sequential
# import serial
# import serial.tools.list_ports


class MCHandleTrainer:

    def __init__(self, root=None):
        self.root = root
        if self.root is None:
            self.root = Tk()
        self.port = ''
        self.bps = 115200
        self.serial = None

        self.init_port = StringVar()
        self.init_bps = StringVar()
        self.init_com_left = StringVar()
        self.init_com_right = StringVar()

        self.init_top = Toplevel()
        self.init_communication()
        message = Label(self.root, text='请先设置')
        message.grid(row=0, column=0)

        # message.grid_forget()

    def init_communication(self):
        top = self.init_top
        frame = LabelFrame(top, text="连接设置")
        Label(frame, text="左手柄").grid(row=1, column=1)
        Entry(frame, textvariable=self.init_com_left).grid(row=1, column=2)
        Label(frame, text="右手柄").grid(row=2, column=1)
        Entry(frame, textvariable=self.init_com_right).grid(row=2, column=2)
        Label(frame, text="波特率").grid(row=3, column=1)
        Entry(frame, textvariable=self.init_bps).grid(row=3, column=2)
        frame.grid(row=1, columnspan=3, column=1)

        Button(top, text="测试", command=self.init_communication_test).grid(row=2, column=1, sticky=W+E)
        Button(top, text="刷新", command=self.init_communication_refresh).grid(row=2, column=2, sticky=W+E)
        Button(top, text="确定", command=self.init_communication_ok).grid(row=2, column=3, sticky=W+E)
        top.mainloop()

    def init_communication_ok(self):
        try:
            bps = int(self.init_bps.get())
        except ValueError:
            messagebox.showerror("错误", '数值错误！')
            return
        self.bps = bps
        self.init_top.destroy()

    def mainloop(self):
        self.root.mainloop()

    def init_communication_test(self):
        pass

    def init_communication_refresh(self):
        pass


if __name__ == '__main__':
    _trainer = MCHandleTrainer()
    # _trainer.init_communication()
    _trainer.mainloop()
