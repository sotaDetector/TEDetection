from tedVision.common.detectionResult import detectionResultPool, detectionFrame
import abc
import threading
import cv2
import time


class sotModuleBase(detectionResultPool):

    def __init__(self):
        super().__init__()
        self.isTracking=False

    @abc.abstractmethod
    def objectTracking(self,frame) -> detectionFrame:
        pass

    @abc.abstractmethod
    def selectTrackObject(self):
        pass

    @abc.abstractmethod
    def resourceRelease(self):
        pass

    def setupDatasource(self, sourceType: int, sourceData):
        self.sourceType = sourceType
        self.sourceData = sourceData

    def getCapSize(self):
        while(self.cap is None):
            time.sleep(0.1)
        return self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __tracking_thread(self):
        while self.isTracking:
            flag,frame=self.cap.read()
            trackingResult=self.objectTracking(frame)
            self._pushDctFrameData(trackingResult)

    def startTracking(self):
        self.isTracking=True
        self.cap=cv2.VideoCapture(self.sourceData)

        threading.Thread(target=self.__tracking_thread).start()

    def stopTracking(self):
        self.isTracking=False
        self.resourceRelease()




