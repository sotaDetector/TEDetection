from enum import Enum, unique

@unique
class RTCModel(Enum):
    SED_RECV = 1
    SED_ONLY = 2
    RECV_ONLY = 3

class SignDT(Enum):
    SIG_DT_MESSAGE="message"
    SIG_DT_JOIN = "join"
    SIG_DT_LEAVE = "leave"


