from enum import Enum, unique

@unique
class RTCModel(Enum):
    SED_RECV = 1
    SED_ONLY = 2
    RECV_ONLY = 3

class SignDT(Enum):
    SIG_DT_MESSAGE="message"
    SING_DT_JOIN = "join"
    SING_DT_LEAVE = "leave"

    SING_SERVER_JOINED="joined"
    # other joined
    SING_SERVER_OTHER_JOINED = 'otherJoined'
    # self leaved
    SING_SERVER_LEAVED = 'leaved'
    # other leaved the room
    SING_SERVER_OTHER_LEAVED = 'otherLeaved'

