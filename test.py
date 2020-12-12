from threading import Thread
from collections import deque
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


class webcam:
    """
    A class that will detect face and eyes
    """
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.flag = True

    def detect_face(self):
        while True:
            ret, frame = self.cap.read()
            frame = cv2.add(frame, np.array([30.0]))
            face_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detected = False
            face_rectangle = face_cascade.detectMultiScale(face_img, scaleFactor=1.4, minNeighbors=5)
            for (x, y, w, h) in face_rectangle:
                cv2.rectangle(face_img, (x, y), (x + w, y + h), (255, 255, 255), 5)
                detected = True
                face = face_img[y:y + h, x:x + w]  # cropping the face rectangle
                eyes_rectangle = eye_cascade.detectMultiScale(face)  # detection for eyes in the face
                for (xx, yy, ww, hh) in eyes_rectangle:
                    cv2.rectangle(face_img, (xx + x, y + yy), (x + xx + ww, y + yy + hh), (255, 0, 0), 2)  # drawing rectangle over the detected eyes

            cv2.imshow('face detect', face_img)
            cv2.waitKey(1)
            self.flag = detected

    def start(self):
        Thread(target=self.detect_face,args=()).start();
        return self

    def __del__(self):
        self.cap.release()


path = '/home/devil/Downloads/vv.mp4'
#PlayVideo(path)
wb = webcam()
wb.detect_face().start()

