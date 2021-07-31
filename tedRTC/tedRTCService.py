from common.logManager import logUtils
from tedSignallingSys.commonUtils.dataFlags import commonDataTag
from tedRTC.signallingClient.socketioClient import socketioClient


class sigDataDispacher:

    def initEventListener(self):

        socketioClient.sioClient.on(commonDataTag.SING_JOINED, self.joinedRoom)

        socketioClient.sioClient.on(commonDataTag.SING_OTHER_JOINED, self.otherJoined)

        socketioClient.sioClient.on(commonDataTag.SING_LEAVED, self.leavedRoom)

        socketioClient.sioClient.on(commonDataTag.SING_OTHER_LEAVED, self.otherLeaved)

        socketioClient.sioClient.on(commonDataTag.SING_MESSAGE, self.onMessage)

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
    sigDataDispacher().initEventListener()
    socketioClient.sendSigData("join","123","user01",{})

