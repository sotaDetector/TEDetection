from tedCore.objectDetection.yolov5Module import yolov5Module
import cv2

yolov5Mou=yolov5Module()

yolov5Mou.setupDatasource(1,0)

yolov5Mou.startDetect()


while True:
    detectionFrame=yolov5Mou.getDctFrameData()
    if detectionFrame is not None:
        cv2.imshow("show",detectionFrame.dctImg)
        print(detectionFrame.dctResult.print())
        cv2.waitKey(1)