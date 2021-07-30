from enum import Enum, unique

@unique
class RTCModel(Enum):
    SED_RECV = 1
    SED_ONLY = 2
    RECV_ONLY = 3


