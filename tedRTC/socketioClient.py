import socketio

from tedSignallingSys.commonUtils.dataFlags import commonDataTag
from tedSignallingSys.commonUtils.logManager import logUtils
from tedRTC.RTCCore.rtcClient import rtcClient

rtcClient=rtcClient()

class socketioClient:

    def __init__(self,ip:str,port:int):
        self.sioClient = socketio.Client()
        self.sioClient.connect(url="http://"+ip+":"+str(port))
        logUtils.info("create socketio client succssfully")


    def sendSigData(self,eventType,roomId,userId,data):
        self.sioClient.emit(eventType,{
            "roomId": roomId,
            "userId": userId,
            "data": data
        })


class sigDataDispacher:

    def __init__(self,socketClienrt:socketioClient):
        self.sioClient=socketClienrt

    def initEventListener(self):

        self.sioClient.on(commonDataTag.SING_JOINED, self.joinedRoom)

        self.sioClient.on(commonDataTag.SING_OTHER_JOINED, self.otherJoined)

        self.sioClient.on(commonDataTag.SING_LEAVED, self.leavedRoom)

        self.sioClient.on(commonDataTag.SING_OTHER_LEAVED, self.otherLeaved)

        self.sioClient.on(commonDataTag.SING_MESSAGE, self.onMessage)

    def joinedRoom(self,data):
        logUtils.info("join the room")
        logUtils.info(data);


    def otherJoined(self,data):
        logUtils.info("other joined")
        logUtils.info(data);


    def leavedRoom(self,data):
        logUtils.info("leaved the room")
        logUtils.info(data);

    def otherLeaved(self,data):
        logUtils.info("other leaved")
        logUtils.info(data);


    def onMessage(self,data):
        logUtils.info("message")
        logUtils.info(data);


if __name__=="__main__":
    client=socketioClient("192.168.1.7",3660)
    sigDispacher=sigDataDispacher(client.sioClient)
    sigDispacher.initEventListener()

    client.sendSigData("join","123","user1",{})

    client.sioClient.wait()