import numpy as np
import abc
import av


class videoTransformBase(abc.ABC):

    @abc.abstractmethod
    def transform(self, frame: av.VideoFrame) -> np.ndarray:
        """return a new frame video frame by bgr24 format"""
        raise NotImplementedError("transform() is not implemented")

    def recv(self,frame:av.VideoFrame)->av.VideoFrame:

        new_image=self.transform(frame)
        return av.VideoFrame.from_ndarray(new_image,format="bgr24")
