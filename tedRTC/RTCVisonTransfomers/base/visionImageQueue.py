import queue


class roomFrameQueue:
    default_queue_size = 24
    roomFrameQueueMap = {}
    lastFrame={}

    @staticmethod
    def pushImageToQueue(cls, roomId: str, frame):
        cls.lastFrame[roomId]=frame
        if not cls.roomFrameQueueMap.keys().__contains__(roomId):
            new_queue = queue.Queue(maxsize=cls.default_queue_size)
            cls.roomFrameQueueMap[roomId] = new_queue

        # clear if the queue is full
        if cls.roomFrameQueueMap[roomId].qsize() >= cls.default_queue_size:
            cls.roomFrameQueueMap[roomId].queue.clear()

        cls.roomFrameQueueMap[roomId].put_nowait(frame)

    @staticmethod
    def getImageFromQueue(cls, roomId):

        if not cls.roomFrameQueueMap.keys().__contains__(roomId):
            return None
        try:
            return cls.roomFrameQueueMap[roomId].get_nowait()
        except:
            return cls.lastFrame[roomId]
