import torch
from tedVision.common.detectionModule import detectionModuleBase
from tedVision.common.detectionResult import detectionFrame



class yolov5Module(detectionModuleBase):


    def __init__(self,modelConfig):
        super().__init__(modelConfig) #the method must be called
        # self.model = torch.hub.load('E://visionProject/TEDetection/resources/modelWeights/yolov5s.pt', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom


    #the yolov5 init method
    def _loadModel(modelConfig):
        pass



    def _detectionEngine(self,frameData):
        results = self.model(frameData)
        return detectionFrame(frameData,results)

    def resourceRelease(self):
        pass

