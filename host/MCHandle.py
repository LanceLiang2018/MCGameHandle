from tkinter import *
from tkinter import messagebox
from host.BaseComm import BaseComm


class MCHandle:
    ACTION_NONE = '无动作'
    ACTION_FORWARD = '前进'
    ACTION_JUMP = '起跳'
    ACTION_DOWN = '下降'
    ACTION_HIT = '打击'
    ACTION_PUT = '放置'
    ACTIONS = [ACTION_NONE, ACTION_FORWARD, ACTION_JUMP, ACTION_DOWN, ACTION_HIT, ACTION_PUT]

    def __init__(self, root=None):
        self.init_top = Tk()

        self.init_bps = StringVar()
        self.init_bps.set('115200')
        self.init_com_left = StringVar()
        self.init_com_left.set('COM5')
        self.init_com_right = StringVar()
        self.init_com_right.set('COM9')

        self.init_communication()

        self.port_left = 'COM5'
        self.port_right = 'COM9'
        self.bps = 115200
        self.comm = None
        self.n = 512
        self.select = 64
        self.frames = [[0 for i in range(12)] for j in range(self.n)]

        # 建立网络
        self.model_file = 'mc_actions.h5'

        # 建立网络的过程放在线程2

        # self.model = model
        # print(self.model.get_config())

        self.comm_left = BaseComm(self.init_com_left.get(), self.bps)
        self.comm_right = BaseComm(self.init_com_right.get(), self.bps)

        self.root = root
        if self.root is None:
            self.root = Tk()
        self.root.title("MC手柄训练器")

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

        Button(top, text="测试", command=self.init_communication_test).grid(row=2, column=1, sticky=W + E)
        Button(top, text="刷新", command=self.init_communication_refresh).grid(row=2, column=2, sticky=W + E)
        Button(top, text="确定", command=self.init_communication_ok).grid(row=2, column=3, sticky=W + E)
        top.mainloop()

    def init_communication_ok(self):
        try:
            bps = int(self.init_bps.get())
        except ValueError:
            messagebox.showerror("错误", '数值错误！')
            return
        self.bps = bps
        self.port_left = self.init_com_left.get()
        self.port_right = self.init_com_right.get()
        if self.init_communication_test(show=False) is False:
            messagebox.showerror("错误", '手柄测试不通过！')
            return
        self.init_top.destroy()

    def mainloop(self):
        self.root.mainloop()

    def init_communication_test(self, show=True):
        try:
            bps = int(self.init_bps.get())
        except ValueError:
            messagebox.showerror("错误", '数值错误！')
            return
        res = True
        print('测试左手柄')
        comm = BaseComm(self.init_com_left.get(), bps)
        if not comm.test():
            if show is True:
                messagebox.showerror("错误", '测试左手柄失败')
            res = False
        comm.close()
        print('测试右手柄')
        comm = BaseComm(self.init_com_right.get(), bps)
        if not comm.test():
            if show is True:
                messagebox.showerror("错误", '测试右手柄失败')
            res = False
        comm.close()
        return res

    def init_communication_refresh(self):
        pass

if __name__ == '__main__':
    _handle = MCHandle()
    _handle.mainloop()
