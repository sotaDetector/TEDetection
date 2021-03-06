from mmtrack.apis import inference_sot, init_model
from tedVision.common.detectionResult import detectionFrame
from tedVision.common.sotModule import sotModuleBase
import cv2


class SiameseRPNModule(sotModuleBase):

    def __init__(self, configPath: str, weightPath: str, device="cuda:0"):
        super().__init__()
        self.model = init_model(configPath, weightPath, device=device)
        self.frame_id = 0
        self.init_bbox = None

    def objectTracking(self, frame):
        self.frame_id = 1
        if self.init_bbox is None:
            self.selectTrackObject(frame)

        result = inference_sot(self.model, frame, self.init_bbox, self.frame_id)
        box_tracking=result["bbox"]
        cv2.rectangle(frame,(int(box_tracking[0]),int(box_tracking[1])),(int(box_tracking[2]),int(box_tracking[3])),(255,0,0))
        return detectionFrame(frame, result)


    def selectTrackObject(self, frame):
        # reset some value
        self.frame_id = 0
        self.init_bbox = None
        init_bbox = list(cv2.selectROI('SOT_NAME', frame, False, False))
        # convert (x1, y1, w, h) to (x1, y1, x2, y2)
        init_bbox[2] += init_bbox[0]
        init_bbox[3] += init_bbox[1]

        self.init_bbox = init_bbox
        print("select tracking object finished")

    def reselectTracking(self):
        self.init_bbox=None

    def resourceRelease(self):
        pass
