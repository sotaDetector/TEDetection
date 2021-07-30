import av
import torch
import cv2

from tedRTC.RTCVisonTransfomers.base.videoTransPlugin_Base import videoTransformBase


class VTP_YOLOV5(videoTransformBase):

    def __init__(self):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom

    def transform(self,frame: av.VideoFrame):
        img = frame.to_ndarray(format="bgr24")
        results = self.model(img)

        for item in results.xyxy[0]:
            arr = item.cpu().numpy()
            cv2.rectangle(img, (int(arr[0]), int(arr[1])), (int(arr[2]), int(arr[3])), (0, 255, 0))

        return img