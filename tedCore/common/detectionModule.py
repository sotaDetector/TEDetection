import abc
import threading
import numpy as np
import cv2

from tedCore.common.detectionResult import detectionResultPool, detectionFrame


class detectionModuleBase(detectionResultPool):

    def __init__(self):
        super().__init__()
        self.isDetect = False

    @abc.abstractmethod
    def _detectionEngine(self,frameData:np.ndarray) -> detectionFrame:
        pass

    @abc.abstractmethod
    def resourceRelease(self):
        pass

    def setDatasource(self,sourceType:int,sourceData):
        self.sourceType=sourceType
        self.sourceData=sourceData

    # private method, only use in this class
    def __detectThread(self):
        while self.isDetect:
            index,frameData=self.cap.read()
            self._pushDctFrameData(self._detectionEngine(frameData))

    def startDetect(self):
        self.isDetect = True
        self.cap=cv2.VideoCapture(self.sourceData)
        threading.Thread(target=self.__detectThread).start()

    def stopDetect(self):
        self.isDetect = False
        self.cap.release()
        self.resourceRelease()
