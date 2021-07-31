import socketio

from common.configPraserUtils import configUtils


class socketioClient:

    sioClient = socketio.Client()
    # sioClient.connect(url="http://"+configUtils.getConfigProperties("socketio","ip")+":"+configUtils.getConfigProperties("socketio","port"))
    sioClient.connect(
        url="http://192.168.1.7:3660")

    @classmethod
    def sendSigData(cls,eventType,roomId,userId,data):
        cls.sioClient.emit(eventType,{
            "roomId": roomId,
            "userId": userId,
            "data": data
        })