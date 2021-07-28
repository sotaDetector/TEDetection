# https://www.cnblogs.com/lanceyu/p/10201236.html
import serial
import threading
import time

class serialCommu:

    def __init__(self):
        serialPort = "COM4"  # 串口
        baudRate = 115200 # 波特率
        self.ser = serial.Serial(serialPort, baudRate,timeout=1)
        print("参数设置：串口=%s ，波特率=%d" % (serialPort, baudRate))

    def sendData(self, data):
        self.ser.write(bytes(str(data),encoding="ASCII"))

    def readData(self):
        while True:
            print(self.ser.readline())


if __name__=="__main__":
    comm=serialCommu()
    for i in range(30):
        comm.sendData(2)
        time.sleep(0.1)
#
