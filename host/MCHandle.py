from tkinter import *
from tkinter import messagebox
from host.BaseComm import BaseComm
import threading
from keras.models import load_model
import time
from host.BaseCtrl import BaseCtrl as ctrl
from host.codemap import VirtualKeyCode
from host.ui_logger import UiLogger
import numpy as np


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
        self.init_com_left.set('COM8')
        self.init_com_right = StringVar()
        self.init_com_right.set('COM9')

        self.init_communication()

        self.port_left = 'COM8'
        self.port_right = 'COM9'
        self.bps = 115200
        self.comm = None
        self.n = 512
        self.select = 64
        self.frames = [[0 for i in range(12)] for j in range(self.n)]

        # 建立网络
        self.model_file = 'mc_actions.h5'

        # 建立网络的过程放在线程2

        # 初始化手柄连接
        self.comm_left = BaseComm(self.init_com_left.get(), self.bps)
        self.comm_right = BaseComm(self.init_com_right.get(), self.bps)

        # 灵敏度
        self.sensitivity = 0.3

        # 先读取几次，读取Init标志
        print('预读取:')
        for i in range(10):
            r1 = self.comm_left.read1epoch()
            r2 = self.comm_right.read1epoch()
            print(r1, r2)

        # 初始化某些变化的值
        # 加上Uilogger
        print('请保持手柄水平放置不动')
        # 初始化遥感的中点值(取平均)       X  Y    X  Y
        self.ave_left, self.ave_right = [0, 0], [0, 0]
        pick = 10
        for i in range(pick):
            data = self.comm_left.read1epoch()
            data_ctrl = data[-4:]
            data_ctrl = list(map(int, data_ctrl))
            self.ave_left[0] += data_ctrl[2] / pick
            self.ave_left[1] += data_ctrl[1] / pick

            data = self.comm_right.read1epoch()
            data_ctrl = data[-4:]
            data_ctrl = list(map(int, data_ctrl))
            self.ave_right[0] += data_ctrl[2] / pick
            self.ave_right[1] += data_ctrl[1] / pick

        print('初始化遥感中点:', self.ave_left, self.ave_right)

        self.root = root
        if self.root is None:
            self.root = Tk()
        self.root.title("MC手柄")

        self.logger = UiLogger(self.root, height=10, width=32)
        self.logger.logger().grid(row=1, column=1, sticky=W+E)

        self.lock = threading.Lock()

        t = threading.Thread(target=self.run_thread)
        t.setDaemon(True)
        t.start()

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

    # 第二个线程，负责读取->应用
    def run_thread(self):
        # 读取神经网络模型
        model = load_model(self.model_file)

        t2 = 0

        click = False
        key1 = ctrl.ACTION_NONE
        key2 = ctrl.ACTION_NONE
        jump = ctrl.ACTION_NONE

        while True:
            time.sleep(0.01)

            data_left = self.comm_left.read1epoch()
            data_right = self.comm_right.read1epoch()

            # 右手处理
            right_ctrl = data_right[-4:]
            right_ctrl = list(map(int, right_ctrl))
            ctrl.move((right_ctrl[2] - self.ave_left[0]) * self.sensitivity,
                      (right_ctrl[1] - self.ave_left[1]) * self.sensitivity)
            if right_ctrl[0] == 0 and click is False:
                ctrl.left_down()
                click = True
            if right_ctrl[0] == 1 and click is True:
                ctrl.left_up()
                click = False
            # Jump
            if data_left[6] == 0 and jump == ctrl.ACTION_NONE:
                jump = ctrl.ACTION_UP
                ctrl.kbd_down(VirtualKeyCode.SPACEBAR)
                # ctrl.kbd_click(VirtualKeyCode.SPACEBAR)
            if data_left[6] == 1 and jump == ctrl.ACTION_UP:
                jump = ctrl.ACTION_NONE
                ctrl.kbd_up(VirtualKeyCode.SPACEBAR)
                # ctrl.kbd_click(VirtualKeyCode.SPACEBAR)

            # 左手处理
            pos = data_left[-4:][1:3]
            # Right
            if pos[1] > 800 and key1 == ctrl.ACTION_NONE:
                key1 = ctrl.ACTION_D
                ctrl.kbd_down(VirtualKeyCode.D_key)
            if pos[1] <= 800 and key1 == ctrl.ACTION_D:
                key1 = ctrl.ACTION_NONE
                ctrl.kbd_up(VirtualKeyCode.D_key)
            # Left
            if pos[1] < 200 and key1 == ctrl.ACTION_NONE:
                key1 = ctrl.ACTION_A
                ctrl.kbd_down(VirtualKeyCode.A_key)
            if pos[1] >= 200 and key1 == ctrl.ACTION_A:
                key1 = ctrl.ACTION_NONE
                ctrl.kbd_up(VirtualKeyCode.A_key)

            # Backward
            if pos[0] < 200 and key2 == ctrl.ACTION_NONE:
                key2 = ctrl.ACTION_W
                ctrl.kbd_down(VirtualKeyCode.W_key)
            if pos[0] >= 200 and key2 == ctrl.ACTION_W:
                key2 = ctrl.ACTION_NONE
                ctrl.kbd_up(VirtualKeyCode.W_key)
            # Forward
            if pos[0] > 800 and key2 == ctrl.ACTION_NONE:
                key2 = ctrl.ACTION_S
                ctrl.kbd_down(VirtualKeyCode.S_key)
            if pos[0] <= 800 and key2 == ctrl.ACTION_S:
                key2 = ctrl.ACTION_NONE
                ctrl.kbd_up(VirtualKeyCode.S_key)

            # 处理神经网络判断
            # frames添加数据
            ann = data_left[0:6]
            ann.extend(data_right[0:6])
            self.lock.acquire()
            self.frames.append(ann)
            self.lock.release()
            # print('ANN DATA:', ann)
            t2 += 1

            # 隔一段时间再判断
            if t2 == 5:
                t2 = 0
                self.lock.acquire()
                x = np.array(self.frames[len(self.frames) - self.select:])
                self.lock.release()
                x = x.reshape((1, x.size))
                # print('X shape:', x.shape)
                # res = model.train_on_batch(x=x, y=y)
                predict = model.predict(x=x)[0]
                predict = predict.tolist()
                res = predict.index(max(predict))
                res = self.ACTIONS[res]
                # print('predict:', res)
                self.logger.push(UiLogger.Item(UiLogger.LEVEL_INFO, 'predict', '%s' % res))


if __name__ == '__main__':
    _handle = MCHandle()
    _handle.mainloop()
