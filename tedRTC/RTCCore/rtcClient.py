from aiortc import RTCPeerConnection, RTCConfiguration, RTCIceServer, MediaStreamTrack

from common.configPraserUtils import configUtils
from common.constantDataUtils import RTCModel
from common.logManager import logUtils
from tedRTC.RTCVisonTransfomers.base.videoTransPlugin_Base import videoTransformBase


class rtcClient:

    def __init__(self, roomId: str, visionPlugin: videoTransformBase, RTCModel: RTCModel):
        self.roomId = roomId
        self.visionTransPlugin = visionPlugin
        self.RTCModel = RTCModel

        #1.create perrconnection
        self.pc=self.createPeerConnection({
            "urls":configUtils.getConfigProperties("stun","urls"),
            "username":configUtils.getConfigProperties("stun","username"),
            "credential":configUtils.getConfigProperties("credential","urls")
        })

        #2.bind pc callback event
        self.bindPCEvent()



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

    def bindMediaTrack(self,inputTrack:MediaStreamTrack):
        logUtils.info("bind media track start...")
        input_track_kind=inputTrack.kind
        logUtils.info("input media track type:" + input_track_kind)

        if input_track_kind == "video":
            out_track = AsyncVideoTransformTrack(track=inputTrack, video_transformer=self.visionTransPlugin,
                                                 roomId=self.roomId)
        elif input_track_kind == "audio":
            out_track = inputTrack

        self.pc.addTrack(out_track)
        logUtils.info("bind media track end...")


    def bindPCEvent(self):
        @self.pc.on("track")
        def on_track(input_track):
            self.bindMediaTrack(input_track)




print(configUtils.getConfigProperties("stun","urls"))