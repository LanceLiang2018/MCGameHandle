from host.BaseCtrl import BaseCtrl
from host.BaseComm import BaseComm
import time

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
#     ctrl.move(int((data[1] - 504) * dig), int((1024 - data[2] - 521) * dig))
#
#     if data[0] == 0 and click is False:
#         ctrl.left_down()
#         click = True
#     if data[0] == 1 and click is True:
#         ctrl.left_up()
#         click = False


key =

# 左手部分
while True:
    time.sleep(0.01)
    data = comm.read1epoch()[-4:]
    data = list(map(int, data))
    print(data)

    pos = data[2:3]
    if pos[0]
