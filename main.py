import cv2
import time
import numpy as np
from datetime import datetime
from threading import Thread

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


class CountsPerSec:
    """
    Class that tracks the number of occurrences ("counts") of an
    arbitrary event and returns the frequency in occurrences
    (counts) per second. The caller must increment the count.
    """

    def __init__(self):
        self._start_time = None
        self._num_occurrences = 0

    def start(self):
        self._start_time = datetime.now()
        return self

    def increment(self):
        self._num_occurrences += 1

    def countsPerSec(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        return self._num_occurrences / elapsed_time


def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame


class webcam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cps = CountsPerSec().start()

    def detect_face(self):
        ret, frame = self.cap.read()
        frame = cv2.add(frame, np.array([30.0]))    # adding brightness to the frame
        face_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                # converting the coloured image into black and white
        detected = False
        face_rectangle = face_cascade.detectMultiScale(face_img, scaleFactor=1.4, minNeighbors=5)  # detecting for face
        for (x, y, w, h) in face_rectangle:
            cv2.rectangle(face_img, (x, y), (x + w, y + h), (255, 255, 255), 5)  # drawing rectangle over the detected face
            detected = True
            face = face_img[y:y + h, x:x + w]  # cropping the face rectangle
            eyes_rectangle = eye_cascade.detectMultiScale(face)  # detection for eyes in the face
            for (xx, yy, ww, hh) in eyes_rectangle:
                cv2.rectangle(face_img, (xx + x, y + yy), (x + xx + ww, y + yy + hh), (255, 0, 0), 2)  # drawing rectangle over the detected eyes
        face_img = putIterationsPerSec(face_img, self.cps.countsPerSec())
        cv2.imshow('face detect', face_img)
        self.cps.increment()
        return detected

    def __del__(self):
        self.cap.release()


class playvideo:
    def __init__(self, path):
        self.movie = cv2.VideoCapture(path)
        self.fps = self.movie.get(cv2.CAP_PROP_FPS)
        self.play = True
        self.cps = CountsPerSec().start()

    def playthevideo(self):
        ret, frame = self.movie.read()
        frame = putIterationsPerSec(frame, self.cps.countsPerSec())
        cv2.imshow('movie', frame)
        self.cps.increment()

    def __del__(self):
        self.movie.release()


seconds = time.time()


def foo(path):
    wb = webcam()
    mv = playvideo(path)

    global seconds
    while True:
        #flag = wb.detect_face()
        flag=True
        if flag and mv.play:
            mv.playthevideo()
            seconds = time.time()

        usr = cv2.waitKey(int(1000 / mv.fps))
        if usr == 32:  # if the user presses the "space"
            mv.play = not mv.play
        if usr == 27 or time.time() - seconds >= 30:  # if the user presses the "esc" key or don't look at screen for a specific time then player stops
            break
    del wb
    del mv
    cv2.destroyAllWindows()


foo('/home/devil/Downloads/video.mp4')
