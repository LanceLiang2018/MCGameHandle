from host.BaseComm import BaseComm
import os
import time
import pyautogui as pag
from ctypes import *
# from win32api import GetSystemMetrics
from host.codemap import VirtualKeyCode
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook
import pyHook
import pythoncom
import threading
import time

dll = WinDLL("C:\\Windows\\System32\\user32.dll")

# x,y = pag.position() # 返回鼠标的坐标
# MC鼠标控制方法：迅速归中

# 初始化屏幕大小
_x , _y = pag.position()
dll.mouse_event(0x0001 | 0x8000, 65536, 65536, 0, 0)
time.sleep(0.01)
display = pag.position()
display = list(map(lambda x: x+1, display))
print('屏幕大小', display)
# pag.position(_x, _y)
dll.mouse_event(0x0001 | 0x8000, int(65536 * _x / display[0]), int(65536 * _y / display[0]), 0, 0)

# 加上小数修正!
fix = [0.0, 0.0]

class BaseCtrl:
    MOUSEEVENTF_MOVE = 0x0001
    # 移动鼠标
    MOUSEEVENTF_LEFTDOWN = 0x0002
    # 模拟鼠标左键按下
    MOUSEEVENTF_LEFTUP = 0x0004
    # 模拟鼠标左键抬起
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    # 模拟鼠标右键按下
    MOUSEEVENTF_RIGHTUP = 0x0010
    # 模拟鼠标右键抬起
    MOUSEEVENTF_MIDDLEDOWN = 0x0020
    # 模拟鼠标中键按下
    MOUSEEVENTF_MIDDLEUP = 0x0040
    # 模拟鼠标中键抬起
    MOUSEEVENTF_ABSOLUTE = 0x8000
    # 标示是否采用绝对坐标
    MOUSEEVENTF_WHEEL = 0x0800
    # 鼠标滚轮
    WHEEL_DELTA = 120
    # 一次滚动
    KEYEVENTF_KEYUP = 0x0002
    # 按键抬起
    KEYEVENTF_EXTENDEDKEY = 0x0001
    # 按键单击

    ACTION_NONE = 0
    ACTION_W = 1
    ACTION_S = 2
    ACTION_A = 3
    ACTION_D = 4
    ACTION_E = 5
    ACTION_UP = 6
    ACTION_DOWN = 7

    def __init__(self):
        pass

    @staticmethod
    # 传入数据：长度4 [x, y, key1, key2]
    def parse(data: list):
        if len(data) != 4:
            return

    @staticmethod
    def move(x, y):
        global fix
        # 使用相对位置
        # 范围：[1, 1, 屏幕宽度-1, 屏幕高度-1]
        # x = int(x * 65535 / display[0])
        # y = int(y * 65535 / display[1])
        ix, iy = int(x), int(y)
        fix[0] = fix[0] + (x - ix)
        fix[1] = fix[1] + (y - iy)
        if fix[0] >= 1:
            fix[0] -= 1
            ix += 1
        if fix[0] <= -1:
            fix[0] += 1
            ix -= 1

        if fix[1] >= 1:
            fix[1] -= 1
            iy += 1
        if fix[1] <= -1:
            fix[1] += 1
            iy -= 1
        ix = int(ix * 50 / display[0])
        iy = int(iy * 50 / display[1])
        print('fix:', fix)
        # dll.mouse_event(BaseCtrl.MOUSEEVENTF_ABSOLUTE | BaseCtrl.MOUSEEVENTF_MOVE, x, y, 0, 0)
        dll.mouse_event(BaseCtrl.MOUSEEVENTF_MOVE, ix, iy, 0, 0)

    @staticmethod
    def left_down():
        dll.mouse_event(BaseCtrl.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    @staticmethod
    def left_up():
        dll.mouse_event(BaseCtrl.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    @staticmethod
    def right_down():
        dll.mouse_event(BaseCtrl.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)

    @staticmethod
    def right_up():
        dll.mouse_event(BaseCtrl.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    @staticmethod
    def wheel_up():
        dll.mouse_event(BaseCtrl.MOUSEEVENTF_WHEEL, 0, 0, BaseCtrl.WHEEL_DELTA, 0)

    @staticmethod
    def wheel_down():
        # 取反表示负数
        dll.mouse_event(BaseCtrl.MOUSEEVENTF_WHEEL, 0, 0, ~BaseCtrl.WHEEL_DELTA, 0)

    @staticmethod
    def kbd_down(code: int):
        dll.keybd_event(int(code), 0, 0, 0)

    @staticmethod
    def kbd_up(code: int):
        dll.keybd_event(code, 0, BaseCtrl.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def kbd_click(code: int):
        dll.keybd_event(code, 0, BaseCtrl.KEYEVENTF_EXTENDEDKEY, 0)
        # dll.keybd_event(int(code), 0, 0, 0)
        # time.sleep(0.01)
        # dll.keybd_event(code, 0, BaseCtrl.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def action_forward_down():
        BaseCtrl.kbd_down(VirtualKeyCode.W_key)

    @staticmethod
    def action_forward_up():
        BaseCtrl.kbd_up(VirtualKeyCode.W_key)

    @staticmethod
    def action_backward_down():
        BaseCtrl.kbd_down(VirtualKeyCode.S_key)

    @staticmethod
    def action_backward_up():
        BaseCtrl.kbd_up(VirtualKeyCode.S_key)

    @staticmethod
    def action_left_down():
        BaseCtrl.kbd_down(VirtualKeyCode.S_key)

    @staticmethod
    def action_left_up():
        BaseCtrl.kbd_up(VirtualKeyCode.S_key)

    @staticmethod
    def action_right_down():
        BaseCtrl.kbd_down(VirtualKeyCode.S_key)

    @staticmethod
    def action_right_up():
        BaseCtrl.kbd_up(VirtualKeyCode.S_key)
    @staticmethod
    def action_up_down():
        BaseCtrl.kbd_down(VirtualKeyCode.S_key)

    @staticmethod
    def action_up_up():
        BaseCtrl.kbd_up(VirtualKeyCode.S_key)

    @staticmethod
    def action_down_down():
        BaseCtrl.kbd_down(VirtualKeyCode.S_key)

    @staticmethod
    def action_down_up():
        BaseCtrl.kbd_up(VirtualKeyCode.S_key)

    @staticmethod
    def item_bar():
        BaseCtrl.kbd_click(VirtualKeyCode.E_key)

    @staticmethod
    def hot_key(function):
        class KeyboardMgr:
            m_bZeroKeyPressed = False
            m_bShiftKeyPressed = False

            def on_key_pressed(self, event):
                if str(event.Key) == 'Lshift' or str(event.Key) == 'Rshift' and self.m_bZeroKeyPressed != True:
                    self.m_bShiftKeyPressed = True
                if event.Alt == 32 and str(event.Key) == 'Z' and self.m_bShiftKeyPressed == True:
                    function()
                return True

            def on_key_up(self, event):
                if str(event.Key) == 'Lshift' or str(event.Key) == 'Rshift':
                    self.m_bShiftKeyPressed = False
                elif str(event.Key) == 'Z':
                    self.m_bZeroKeyPressed = False
                return True

        keyMgr = KeyboardMgr()
        hookMgr = pyHook.HookManager()
        hookMgr.KeyDown = keyMgr.on_key_pressed
        hookMgr.KeyUp = keyMgr.on_key_up
        hookMgr.HookKeyboard()
        pythoncom.PumpMessages()

    @staticmethod
    # 按下热键的时候的处理
    def when_hot_key(function):
        t = threading.Thread(target=BaseCtrl.hot_key, args=(function, ))
        t.setDaemon(True)
        t.start()

if __name__ == '__main__':
    # BaseCtrl.when_hot_key(lambda: print('HOT'))
    # time.sleep(10)
    BaseCtrl.move(65536 // 10, 65536 // 10)
