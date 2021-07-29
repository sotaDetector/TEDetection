from flask_socketio import emit

from tedSignallingSys.commonUtils.logUtils import logUtils


class socketService:
    # define the signallings
    # joined self
    SING_JOINED = 'joined'
    # other joined
    SING_OTHER_JOINED = 'otherJoined'
    # self leaved
    SING_LEAVED = 'leaved'
    # other leaved the room
    SING_OTHER_LEAVE = 'otherLeaved'
    # common message
    SING_MESSAGE = "message"

    # send msg to all in the room bu self
    @staticmethod
    def send_to_other(eventType, roomId, data):
        emit(eventType, data, room=roomId, include_self=False)
        logUtils.info("send_to_other:eventType=" + eventType + ",roomId=" + roomId + ",data=" + str(data))

    # send to self
    @staticmethod
    def send_to_self(eventType, data):
        emit(eventType, data)
        logUtils.info("send_to_self eventType=" + eventType + ",data=" + str(data))

    # send to all
    @staticmethod
    def send_to_all(eventType, roomId, data):
        emit(eventType, data, room=roomId)
        logUtils.info("send_to_all:eventType=" + eventType + ",roomId=" + roomId + ",data=" + str(data))
