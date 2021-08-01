from aiortc import MediaStreamTrack
import av
import queue

from tedRTC.RTCVisonTransfomers.base.videoTransPlugin_Base import videoTransformBase
from tedRTC.RTCVisonTransfomers.base.visionImageQueue import roomFrameQueue


class visionTransFromMediaTrack(MediaStreamTrack):
    kind="video"
    def __init__(self,roomId:str, track: MediaStreamTrack, visionTransPlugin: videoTransformBase):
        super().__init__()
        self.track = track
        self.transformers = visionTransPlugin
        self.roomId=roomId

    async def recv(self):
        # get orign data
        frame = await self.track.recv()
        # trans
        # rebuild a av.VideoFrame,processing timing information
        new_frame = av.VideoFrame.from_ndarray(self.transformers.transform(frame),
                                               format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base

        roomFrameQueue.pushImageToQueue(roomId=self.roomId,frame=new_frame)
        return new_frame


class visionMonitorTrackBase(MediaStreamTrack):
    kind = "video"

    def __init__(self,roomId:str):
        super().__init__()
        self.roomId=roomId

    async def recv(self):
        # pts, time_base = await self.next_timestamp()
        # frame.pts = pts
        # frame.time_base = time_base
        frame=roomFrameQueue.getImageFromQueue(self.roomId)
        return frame







