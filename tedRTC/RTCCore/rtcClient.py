from aiortc import RTCPeerConnection, RTCConfiguration, RTCIceServer, MediaStreamTrack, RTCSessionDescription
from aiortc.rtcicetransport import candidate_from_aioice
from aiortc.sdp import candidate_from_sdp
from common.configPraserUtils import configUtils
from common.constantDataUtils import ClientType, SignDT
from common.logManager import logUtils
from tedRTC.RTCVisonTransfomers.base.videoTransPlugin_Base import videoTransformBase
from tedRTC.RTCVisonTransfomers.base.visionTransFactory import visionTransFromMediaTrack, visionMonitorTrackBase
from tedRTC.signallingClient.socketioClient import socketioClient


class rtcClient:

    """
        clientType:1 普通客户端 default
        clientType:2 监控端
    """
    def __init__(self, roomId: str,visionTransPlugin: videoTransformBase=None, cliType: ClientType=ClientType.SED_RECV):
        self.roomId = roomId
        self.visionTransPlugin = visionTransPlugin
        self.cliType = cliType

        # 1.create perrconnection
        self.pc = self.createPeerConnection({
            "urls": configUtils.getConfigProperties("stun", "urls"),
            "username": configUtils.getConfigProperties("stun", "username"),
            "credential": configUtils.getConfigProperties("stun", "credential")
        })

        # 2.bind pc callback event
        self.bindPCEvent()

    # create rtc peer connection
    def createPeerConnection(self, stunConfig):
        logUtils.info("create rtcPeerConnection start...")
        return RTCPeerConnection(configuration=RTCConfiguration(
            iceServers=[
                RTCIceServer(
                    urls=stunConfig["urls"],
                    username=stunConfig["username"],
                    credential=stunConfig["credential"]
                )
            ]
        ))

        logUtils.info("create rtcPeerConnection end...")

    # bind event for pc
    def bindPCEvent(self):
        @self.pc.on("track")
        def on_track(input_track):
            self.bindMediaTrack(input_track)

            @input_track.on("ended")
            async def on_ended():
                logUtils.info("media track transport ended...")

        #监控端添加track,因为客户端只接受媒体，所以无法出发@input_track方法，只能放这里
        if self.cliType==ClientType.RECV_ONLY:
            out_track=visionMonitorTrackBase(roomId=self.roomId)
            self.pc.addTrack(out_track)

        @self.pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            logUtils.info("ICE connection state is %s" + self.pc.iceConnectionState)
            if self.pc.iceConnectionState == "failed":
                await self.pc.close()

    async def processOffer(self, roomId: str, offerDict):
        await self.setRemoteOffer(offerDict)

        await self.createAnswer()

        # send the answer sdp to socket server
        socketioClient.sendSigData(eventType=SignDT.SIG_DT_MESSAGE.value,
                                   roomId=roomId,
                                   data={
                                       "type": self.pc.localDescription.type,
                                       "sdp": self.pc.localDescription.sdp
                                   }
                                   )

    # set remote answer
    async def setRemoteOffer(self, offerDict):
        logUtils.info("set remote offer start...")

        rtc_offer = self.getRTCSessionDescription(offerDict["sdp"], offerDict["type"])
        await self.pc.setRemoteDescription(rtc_offer)

        logUtils.info("set remote offer end...")

    async def createAnswer(self):
        logUtils.info("create answer start...")

        answer = await self.pc.createAnswer()
        await self.pc.setLocalDescription(answer)
        logUtils.info(self.pc.localDescription)

        logUtils.info("create answer end...")

    def bindMediaTrack(self, inputTrack: MediaStreamTrack):
        logUtils.info("bind media track start...")
        out_track = None
        input_track_kind = inputTrack.kind
        logUtils.info("input media track type:" + input_track_kind)

        if self.cliType==ClientType.SED_RECV:
            if input_track_kind == "video":
                out_track = visionTransFromMediaTrack(roomId=self.roomId,track=inputTrack, visionTransPlugin=self.visionTransPlugin)
            elif input_track_kind == "audio":
                out_track = inputTrack


        self.pc.addTrack(out_track)

        logUtils.info("bind media track end...")

    async def setCandidate(self, data):
        print("接收到candidate")
        print(data["candidate"])
        RTCIceCandidate=candidate_from_sdp(data["candidate"])
        RTCIceCandidate.sdpMid=data['sdpMid']
        RTCIceCandidate.sdpMLineIndex=data["sdpMLineIndex"]
        print(RTCIceCandidate)
        await self.pc.addIceCandidate(RTCIceCandidate)

    # package to RtcSessionDescription format
    def getRTCSessionDescription(self, sdp, type):
        return RTCSessionDescription(sdp=sdp, type=type)
