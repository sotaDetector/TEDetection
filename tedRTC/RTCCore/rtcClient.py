from aiortc import RTCPeerConnection, RTCConfiguration, RTCIceServer

from common.constantDataUtils import RTCModel
from tedRTC.RTCVisonTransfomers.base.videoTransPlugin_Base import videoTransformBase


class rtcClient:

    def __init__(self, roomId: str, visionPlugin: videoTransformBase, RTCModel: RTCModel):
        self.rooId = roomId
        self.visionPlugin = visionPlugin
        self.RTCModel = RTCModel

        #1.create perrconnection
        self.pc=self.createPeerConnection({
            "urls":"turn:iclockmaker.com:3478",
            "username":"tvs",
            "credential":"158246"
        })



    # create rtc peer connection
    def createPeerConnection(self, stunConfig):
        return RTCPeerConnection(configuration=RTCConfiguration(
            iceServers=[
                RTCIceServer(
                    urls=stunConfig["urls"],
                    username=stunConfig["username"],
                    credential=stunConfig["credential"]
                )
            ]
        ))
