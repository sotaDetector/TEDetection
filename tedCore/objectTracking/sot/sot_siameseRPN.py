from mmtrack.apis import inference_sot, init_model
from tedCore.common.detectionResult import detectionFrame
from tedCore.common.sotModule import sotModuleBase
import cv2


class SiameseRPN(sotModuleBase):

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


if __name__ == "__main__":
    configPath = "../../../excellentDependency/mmtracking/configs/sot/siamese_rpn/siamese_rpn_r50_1x_lasot.py"
    weightPath = "../../../resources/modelWeights/siamese_rpn_r50_1x_lasot_20201218_051019-3c522eff.pth"
    siameseSot = SiameseRPN(configPath, weightPath)
    siameseSot.setupDatasource(1, 0)
    siameseSot.startTracking()
    print("-------------------------")

    while True:
        detResult=siameseSot.getDctFrameData()
        if detResult is not None:
            cv2.imshow("tracking",detResult.dctImg)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                siameseSot.reselectTracking()
