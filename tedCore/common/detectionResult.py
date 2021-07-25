import queue
import numpy as np


class detectItem:

    def __init__(self,dctImg: np.ndarray, dctResult: dict):
        self.dctImg=dctImg
        self.dctResult=dctResult

    def getDctImg(self):
        return self.dctImg

    def getDctResult(self):
        return self.dctResult


class detectionResultPool:

    def __init__(self, poolSize: int = 10):
        self.dctResultQueue = queue.Queue(maxsize=poolSize)

    def pushDctItem(self,dctItem:detectItem):
        self.dctResultQueue.put_nowait(dctItem)

    def getDctItem(self):
        return self.dctResultQueue.get_nowait()
