from tedVision.objectDetection.yolov5Module import yolov5Module
import cv2

class mediaPlayerService:


    def __init__(self):
        self.yolov5Mou = yolov5Module()

        self.yolov5Mou.setupDatasource(1, 0)

        self.yolov5Mou.startDetect()

    def genFramesFromLiveStream(self, sessionId):

        while True:
            detectionFrame = self.yolov5Mou.getDctFrameData()
            ret, buffer = cv2.imencode('.jpg', detectionFrame.dctImg)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

