from common.constantDataUtils import SignDT, ClientType
from common.keyGenerator import keyGen
from common.logManager import logUtils
from tedRTC.RTCCore.rtcClient import rtcClient
from tedRTC.RTCVisonTransfomers.base.videoTransPlugin_Base import videoTransformBase
from tedRTC.RTCVisonTransfomers.visionTransPlugins.visionTransPlugin_YOLOV5 import VTP_YOLOV5
from tedRTC.signallingClient.socketioClient import socketioClient
import asyncio
import time

RTCClientMap = {}
monitorClientMap = {}


class sigDataDispacher:

    def initEventListener(self):

        socketioClient.sioClient.on(SignDT.SING_SERVER_JOINED.value, self.joinedRoom)

        socketioClient.sioClient.on(SignDT.SING_SERVER_OTHER_JOINED.value, self.otherJoined)

        socketioClient.sioClient.on(SignDT.SING_SERVER_LEAVED.value, self.leavedRoom)

        socketioClient.sioClient.on(SignDT.SING_SERVER_OTHER_LEAVED.value, self.otherLeaved)

        socketioClient.sioClient.on(SignDT.SIG_DT_MESSAGE.value, self.onMessage)

    def joinedRoom(self, roomId, data):
        logUtils.info("join the room:" + roomId)
        logUtils.info(data)

    def otherJoined(self, roomId, data):
        logUtils.info("other joined")

    def leavedRoom(self, roomId, data):
        logUtils.info("leaved the room")
        logUtils.info(data);

    def otherLeaved(self, roomId, data):
        logUtils.info("other leaved")
        logUtils.info(data);

    def onMessage(self, roomId, data):

        print("get message:", data)
        if data is not None:
            if data["type"] == "offer":
                if RTCClientMap.keys().__contains__(roomId):
                    loop = asyncio.new_event_loop()
                    loop.create_task(RTCClientMap[roomId].processOffer(roomId, data))

                    try:
                        loop.run_forever()
                    finally:
                        logUtils.info("loop finished...")
                        loop.close()
                elif monitorClientMap.keys().__contains__(roomId):
                    loop = asyncio.new_event_loop()
                    loop.create_task(monitorClientMap[roomId].processOffer(roomId, data))

                    try:
                        loop.run_forever()
                    finally:
                        logUtils.info("loop finished...")
                        loop.close()
            if data["type"] == "candidate":
                if RTCClientMap.keys().__contains__(roomId):
                    loop = asyncio.new_event_loop()
                    loop.run_until_complete(RTCClientMap[roomId].setCandidate(data["data"]))
                    loop.close()
                elif monitorClientMap.keys().__contains__(roomId):
                    loop = asyncio.new_event_loop()
                    loop.run_until_complete(monitorClientMap[roomId].setCandidate(data["data"]))
                    loop.close()





class tedRTClient:

    def __init__(self, roomId: str, clientType: ClientType, visionPlugin: videoTransformBase):
        print("??????tedRTClient")
        if ClientType.SED_RECV == clientType:
            client = rtcClient(roomId=roomId, visionTransPlugin=visionPlugin, cliType=ClientType.SED_RECV)
            RTCClientMap[roomId] = client
        elif ClientType.SED_ONLY == clientType:
            roomId = keyGen.getMonitorRoomId(roomId)
            client = rtcClient(roomId=roomId, cliType=ClientType.SED_ONLY)
            monitorClientMap[roomId] = client
        elif ClientType.RECV_ONLY == clientType:
            client = rtcClient(roomId=roomId,visionTransPlugin=visionPlugin,cliType=ClientType.RECV_ONLY)
            RTCClientMap[roomId] = client

        socketioClient.sendSigData("join", roomId, {})


# if __name__ == "__main__":
    # sigDataDispacher().initEventListener()
    # roomId = "123"
    # tedRTClient(roomId,ClientType.SED_RECV,VTP_YOLOV5())
