import av
import numpy as np
import cv2

from tedRTC.RTCVisonTransfomers.base.videoTransPlugin_Base import videoTransformBase


class VTP_Cartoon(videoTransformBase):

    def transform(self, frame: av.VideoFrame) -> np.ndarray:
        # 1.transform image
        img = frame.to_ndarray(format="bgr24")

        img_color = cv2.pyrDown(cv2.pyrDown(img))
        for _ in range(6):
            img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
        img_color = cv2.pyrUp(cv2.pyrUp(img_color))

        # prepare edges
        img_edges = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img_edges = cv2.adaptiveThreshold(
            cv2.medianBlur(img_edges, 7),
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            9,
            2,
        )
        img_edges = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2RGB)

        # combine color and edges
        img = cv2.bitwise_and(img_color, img_edges)

        return img
