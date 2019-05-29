from host.BaseCtrl import BaseCtrl
from host.BaseComm import BaseComm
import time

port = 'COM6'

comm = BaseComm(port, 115200)
ctrl = BaseCtrl
ctrl.when_hot_key(exit)
# comm.test()
while True:
    time.sleep(0.01)
    data = comm.read1epoch()[-4:]
    data = list(map(int, data))
    print(data)
    ctrl.move(data[1], 1024 - data[2])
