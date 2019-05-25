import serial


class BaseComm:
    def __init__(self, port: str, bps: int, timeout=0.5):
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

    def read1epoch(self):
        line = self.readline()
        split = line.split(',')
        if len(split) != 6:
            return [0 for i in range(6)]
        try:
            split = list(map(float, split))
        except ValueError:
            return [0 for i in range(6)]
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
        if len(line) == 11:
            return self.test()
        return True

    def close(self):
        self.serial.close()


if __name__ == '__main__':
    _bc = BaseComm('COM4', 115200)
    print(_bc.test())
