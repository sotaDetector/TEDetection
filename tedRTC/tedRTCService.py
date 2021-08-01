from common.constantDataUtils import SignDT, RTCModel
from common.logManager import logUtils
from tedRTC.RTCCore.rtcClient import rtcClient
from tedRTC.RTCVisonTransfomers.visionTransPlugins.visionTransPlugin_YOLOV5 import VTP_YOLOV5
from tedRTC.signallingClient.socketioClient import socketioClient
import asyncio
import time

RTCClientMap={}

class sigDataDispacher:

    def initEventListener(self):

        socketioClient.sioClient.on(SignDT.SING_SERVER_JOINED.value, self.joinedRoom)

        socketioClient.sioClient.on(SignDT.SING_SERVER_OTHER_JOINED.value, self.otherJoined)

        socketioClient.sioClient.on(SignDT.SING_SERVER_LEAVED.value, self.leavedRoom)

        socketioClient.sioClient.on(SignDT.SING_SERVER_OTHER_LEAVED.value, self.otherLeaved)

        socketioClient.sioClient.on(SignDT.SIG_DT_MESSAGE.value, self.onMessage)

    def joinedRoom(self,roomId,data):
        logUtils.info("join the room:"+roomId)
        logUtils.info(data)
        client=rtcClient(roomId=roomId,visionTransPlugin=VTP_YOLOV5(),RTCModel=RTCModel.SED_RECV)
        RTCClientMap[roomId]=client

        print("RTCClientMap")
        logUtils.info(RTCClientMap)

    def otherJoined(self,roomId,data):
        logUtils.info("other joined")
        logUtils.info(data);


    def leavedRoom(self,roomId,data):
        logUtils.info("leaved the room")
        logUtils.info(data);

    def otherLeaved(self,roomId,data):
        logUtils.info("other leaved")
        logUtils.info(data);


    def onMessage(self,roomId,data):
        logUtils.info("message")
        logUtils.info(data)

        if data["type"]=="offer":
            if RTCClientMap.keys().__contains__(roomId):
                loop=asyncio.new_event_loop()
                loop.create_task(RTCClientMap[roomId].processOffer(roomId,data))

                try:
                    loop.run_forever()
                finally:
                    logUtils.info("loop finished...")
                    loop.close()


if __name__=="__main__":
    sigDataDispacher().initEventListener()
    socketioClient.sendSigData("join","123",{})

