import serial


class BaseComm:
    def __init__(self, port: str, bps: int, timeout=5):
        self.serial = serial.Serial(port, bps, timeout=timeout)
        self.default_code = 'M'.encode()

    # 规定开始的时候先写入一个字节
    def start_read(self):
        self.serial.write(self.default_code)

    def readline(self):
        self.start_read()
        s = ''
        try:
            c = self.serial.read(1).decode('gbk')
        except ValueError:
            return ''
        while c != '\n':
            s = s + c
            c = self.serial.read(1).decode('gbk')
        return s

    # 数据格式 [ax, ay, az, ag1, ag2, ag3, A1, A2, A3, A6] (10)
    def read1epoch(self):
        line = self.readline()
        if line == 'Init\r':
            return [0 for i in range(10)]
        split = line.split(',')
        # print(split)
        if len(split) != 10:
            print('WARNING: MPU数据长度错误', split)
            return [0 for i in range(10)]
        try:
            split = list(map(float, split))
        except ValueError:
            print('WARNING: MPU数据格式错误', split)
            return [0 for i in range(10)]
        split[0] /= 100
        split[1] /= 100
        split[2] /= 100
        return split

    def test(self):
        print('测试MPU... ')
        # 清空缓冲区
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()

        line = self.readline()
        print('ReadMPU:', line)
        if line == '':
            print('测试失败！')
            return False
        if len(line) == 5:
            return self.test()
        return True

    def close(self):
        self.serial.close()


if __name__ == '__main__':
    _bc = BaseComm('COM4', 115200)
    print(_bc.test())
