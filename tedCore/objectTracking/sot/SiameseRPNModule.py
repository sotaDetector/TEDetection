from tedCore.common.detectionModule import detectionModuleBase
from mmtrack.apis import inference_sot, init_model

class SiameseRPN(detectionModuleBase):
    def __init__(self,configPath:str,weightPath:str):
        super.__init__()
        model = init_model(configPath,weightPath, device="cuda:0")

    def detectionEngine(self,FrameData):
        pass

    def resourceRelease(self):
        pass

