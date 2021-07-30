import numpy as np
import av
import cv2

from tedRTC.RTCVisonTransfomers.base.videoTransPlugin_Base import videoTransformBase


class VTP_EdgeDetect(videoTransformBase):

    def transform(self, frame: av.VideoFrame) -> np.ndarray:
        img = frame.to_ndarray(format="bgr24")
        img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)
        return img

