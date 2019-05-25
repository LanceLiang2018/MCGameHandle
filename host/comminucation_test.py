import serial

ser = serial.Serial('COM4', 115200, timeout=0.5)

ser.write(' '.encode())
ser.read(1)
ser.reset_input_buffer()

while True:
    ser.write(' '.encode())
    s = ''
    try:
        c = ser.read(1).decode('gbk')
    except ValueError:
        continue
    while c != '\n':
        s = s + c
        c = ser.read(1).decode()
    print(s)

