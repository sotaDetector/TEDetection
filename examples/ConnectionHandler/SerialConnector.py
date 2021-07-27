# https://www.cnblogs.com/lanceyu/p/10201236.html
import serial
import threading
import time

class arduinoCommu:

    def __init__(self):
        serialPort = "COM3"  # 串口
        baudRate = 9600  # 波特率
        self.ser = serial.Serial(serialPort, baudRate)
        print("参数设置：串口=%s ，波特率=%d" % (serialPort, baudRate))

    def sendData(self, bytedata):
        self.ser.write(bytedata)

    def readData(self):
        while True:
            print(self.ser.readline())


if __name__=="__main__":
    comm=arduinoCommu()
    for i in range(179):
        value = str(i) + "#90"
        comm.sendData(bytes(value, encoding="utf8"))
        time.sleep(0.1)

