from host.BaseCtrl import BaseCtrl
from host.BaseComm import BaseComm
import time
from host.codemap import VirtualKeyCode

port = 'COM4'

comm = BaseComm(port, 115200)
click = False
ctrl = BaseCtrl
dig = 0.3
ctrl.when_hot_key(exit)
# comm.test()

# # 右手部分
# while True:
#     time.sleep(0.01)
#     data = comm.read1epoch()[-4:]
#     data = list(map(int, data))
#     print(data)
#     ctrl.move((data[1] - 504) * dig, (1024 - data[2] - 521) * dig)
#
#     if data[0] == 0 and click is False:
#         ctrl.left_down()
#         click = True
#     if data[0] == 1 and click is True:
#         ctrl.left_up()
#         click = False


key1 = ctrl.ACTION_NONE
key2 = ctrl.ACTION_NONE
jump = ctrl.ACTION_NONE

# 左手部分
while True:
    time.sleep(0.01)
    data = comm.read1epoch()[-4:]
    data = list(map(int, data))
    # print(data)

    pos = data[1:3]
    # Right
    if pos[0] > 800 and key1 == ctrl.ACTION_NONE:
        key1 = ctrl.ACTION_D
        ctrl.kbd_down(VirtualKeyCode.D_key)
    if pos[0] <= 800 and key1 == ctrl.ACTION_D:
        key1 = ctrl.ACTION_NONE
        ctrl.kbd_up(VirtualKeyCode.D_key)
    # Left
    if pos[0] < 200 and key1 == ctrl.ACTION_NONE:
        key1 = ctrl.ACTION_A
        ctrl.kbd_down(VirtualKeyCode.A_key)
    if pos[0] >= 200 and key1 == ctrl.ACTION_A:
        key1 = ctrl.ACTION_NONE
        ctrl.kbd_up(VirtualKeyCode.A_key)

    # Forward
    if pos[1] > 800 and key2 == ctrl.ACTION_NONE:
        key2 = ctrl.ACTION_W
        ctrl.kbd_down(VirtualKeyCode.W_key)
    if pos[1] <= 800 and key2 == ctrl.ACTION_W:
        key2 = ctrl.ACTION_NONE
        ctrl.kbd_up(VirtualKeyCode.W_key)
    # Backward
    if pos[1] < 200 and key2 == ctrl.ACTION_NONE:
        key2 = ctrl.ACTION_S
        ctrl.kbd_down(VirtualKeyCode.S_key)
    if pos[1] >= 200 and key2 == ctrl.ACTION_S:
        key2 = ctrl.ACTION_NONE
        ctrl.kbd_up(VirtualKeyCode.S_key)

    # Jump
    if data[0] == 0 and jump == ctrl.ACTION_NONE:
        jump = ctrl.ACTION_UP
        ctrl.kbd_down(VirtualKeyCode.SPACEBAR)
        # ctrl.kbd_click(VirtualKeyCode.SPACEBAR)
    if data[0] == 1 and jump == ctrl.ACTION_UP:
        jump = ctrl.ACTION_NONE
        ctrl.kbd_up(VirtualKeyCode.SPACEBAR)
        # ctrl.kbd_click(VirtualKeyCode.SPACEBAR)


    print(pos)
