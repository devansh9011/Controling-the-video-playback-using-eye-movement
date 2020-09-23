import cv2
import time
#import numpy as np
#import matplotlib.pyplot as plt

face_cascade = cv2.CascadeClassifier("/home/devil/PycharmProjects/venv/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier('/home/devil/PycharmProjects/venv/lib/python3.8/site-packages/cv2/data/haarcascade_eye.xml')

def detect_face(img):
    face_img = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                                    # converting the coloured image into black and white
    cv2.imshow('gray', gray)
    detected = False                                                                                # boolean variable to store if face is detected or not
    face_rectangle = face_cascade.detectMultiScale(face_img, scaleFactor=1.4, minNeighbors=5)       # detecting for face
    for (x, y, w, h) in face_rectangle:
        cv2.rectangle(face_img, (x, y), (x + w, y + h), (255, 255, 255), 5)                         # drawing rectangle over the detected face
        detected = True
        face = img[y:y+h, x:x+w]                                                                    # cropping the face rectangle
        eyes_rectangle = eye_cascade.detectMultiScale(face)                                         # detection for eyes in the face
        for (xx, yy, ww, hh) in eyes_rectangle:
            cv2.rectangle(face_img, (xx+x, y+yy), (x+xx + ww, y+yy + hh), (255, 0, 0), 2)           # drawing rectangle over the detected eyes

    return face_img, detected


cap = cv2.VideoCapture(0)
movie = cv2.VideoCapture('/home/devil/Downloads/video.mp4')
play = True
seconds = time.time()

while True:
    ret, frame = cap.read()
    frame, flag = detect_face(frame)
    if flag and play:
        seconds = time.time()
        ret2, frame2 = movie.read()
        cv2.imshow('movie', frame2)
    cv2.imshow('face detect', frame)
    usr = cv2.waitKey(1)
    if usr == 32:                                                       # if the user presses the "space"
        play = not play
    if usr == 27 or time.time()-seconds >= 10:                          # if the user presses the "esc" key or don't look at screen for a specific time then player stops
        break

cap.release()
cv2.destroyAllWindows()

