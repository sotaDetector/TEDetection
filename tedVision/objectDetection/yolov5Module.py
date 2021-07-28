import torch
from tedVision.common.detectionModule import detectionModuleBase
from tedVision.common.detectionResult import detectionFrame



class yolov5Module(detectionModuleBase):


    def __init__(self):
        super().__init__()
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom

    def _detectionEngine(self,frameData):
        results = self.model(frameData)
        return detectionFrame(frameData,results)

    def resourceRelease(self):
        pass
