from threading import Thread
from collections import deque
import cv2


class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.movie = cv2.VideoCapture(src)
        self.fps = self.movie.get(cv2.CAP_PROP_FPS)
        self.grabbed = deque()
        self.frame = deque()
        g, f = self.movie.read()
        self.grabbed.append(g)
        self.frame.append(f)
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            g, f = self.movie.read()
            if not g:
                self.stop()
            else:
                self.frame.append(f)
                self.grabbed.append(g)

    def get_frame(self):
        if len(self.grabbed) != 0:
            g = self.grabbed.popleft()
            f = self.frame.popleft()
            return g, f

    def stop(self):
        self.stopped = True


def threadVideoGet(source):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Main thread shows video frames.
    """

    video_getter = VideoGet(source).start()
    # cps = CountsPerSec().start()
    # print(video_getter.fps)

    while True:
        usr = cv2.waitKey(int(1000))
        if usr == 27 or video_getter.stopped:
            video_getter.stop()
            break
        # if (cv2.waitKey(int(1000 / video_getter.fps)) == ord("q")) or video_getter.stopped:
        #    video_getter.stop()
        #    break

        grabbed, frame = video_getter.get_frame()
        # frame = putIterationsPerSec(frame, cps.countsPerSec())
        cv2.imshow("Video", frame)
        # cps.increment()


path = '/home/devil/Downloads/video.mp4'
threadVideoGet(path)
