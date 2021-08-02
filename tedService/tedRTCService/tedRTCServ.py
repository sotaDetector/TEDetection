from common.constantDataUtils import ClientType
from tedRTC.RTCVisonTransfomers.visionTransPlugins.visionTransPlugin_YOLOV5 import VTP_YOLOV5
from tedRTC.tedRTCClient import sigDataDispacher, tedRTClient


class tedRTCSer:

    def __init__(self):
        sigDataDispacher().initEventListener()

    def createClient(self,roomId):
        tedRTClient(roomId,ClientType.SED_RECV,VTP_YOLOV5())

        return {"rs":1}

    def createMonitorClient(self):
        pass
