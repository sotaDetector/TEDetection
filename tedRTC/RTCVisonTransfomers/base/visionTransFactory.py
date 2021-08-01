from aiortc import MediaStreamTrack
import av

from tedRTC.RTCVisonTransfomers.base.videoTransPlugin_Base import videoTransformBase


class visionTransFromMediaTrack(MediaStreamTrack):
    kind="video"
    def __init__(self, track: MediaStreamTrack, visionTransPlugin: videoTransformBase):
        super().__init__()
        self.track = track
        self.transformers = visionTransPlugin

    async def recv(self):
        # get orign data
        frame = await self.track.recv()
        # trans
        # rebuild a av.VideoFrame,processing timing information
        new_frame = av.VideoFrame.from_ndarray(self.transformers.transform(frame),
                                               format="bgr24")

        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base

        return new_frame
