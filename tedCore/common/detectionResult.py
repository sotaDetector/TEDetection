import queue
import numpy as np


class detectionFrame:

    def __init__(self,dctImg: np.ndarray, dctResult: str):
        self.dctImg=dctImg
        self.dctResult=dctResult

    def getDctImg(self):
        return self.dctImg

    def getDctResult(self):
        return self.dctResult


class detectionResultPool:

    def __init__(self, poolSize: int = 10):
        self.lastFrame=None
        self.poolSize=poolSize
        self.dctResultQueue = queue.Queue(maxsize=poolSize)

    def _pushDctFrameData(self,dctFrame:detectionFrame):
        #if the queue size is bigger than poolsize, then remove the last one to keep the queue latest
        if self.dctResultQueue.qsize()>=self.poolSize:
            self.dctResultQueue.queue.clear()
        self.dctResultQueue.put_nowait(dctFrame)

    def getDctFrameData(self)->detectionFrame:
        if self.dctResultQueue.qsize()>0:
            self.lastFrame=self.dctResultQueue.get_nowait()
        return self.lastFrame
