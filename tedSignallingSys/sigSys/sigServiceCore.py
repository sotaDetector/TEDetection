from flask_socketio import join_room, leave_room

from tedSignallingSys.sigSys.socketService import socketService


class commonDataTag:
    TAG_ROOMId = "roomId"
    TAG_USERID = "userId"
    TAG_DATA = "data"


class sigDataParser:

    def __init__(self, sigData):
        self.roomId = sigData[commonDataTag.TAG_ROOMId]
        self.userId = sigData[commonDataTag.TAG_USERID]
        self.data = sigData[commonDataTag.TAG_DATA]

    def getRoomId(self):
        return self.roomId

    def getUserId(self):
        return self.userId

    def getData(self):
        return self.data


class sigServiceCore:

    def join(self, data):
        sigData = sigDataParser(data)
        # join room

        join_room(sigData.getRoomId())
        # send msg back
        socketService.send_to_self(socketService.SING_JOINED, "server:join room successfully")

        # send msg to others in the room
        socketService.send_to_other(socketService.SING_OTHER_JOINED, sigData.getRoomId(),
                                    "server: other joined: " + sigData.getUserId())
