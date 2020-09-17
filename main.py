import cv2
import numpy as np
import matplotlib.pyplot as plt

#%matplotlib inline

face_cascade = cv2.CascadeClassifier("/home/devil/PycharmProjects/venv/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier('/home/devil/PycharmProjects/venv/lib/python3.8/site-packages/cv2/data/haarcascade_eye.xml')
#smile_cascade = cv2.CascadeClassifier('/home/devil/PycharmProjects/venv/lib/python3.8/site-packages/cv2/data/haarcascade_smile.xml')


def detect_face(img):
    face_img = img.copy()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    face_rectangle = face_cascade.detectMultiScale(face_img, scaleFactor=1.4, minNeighbors=5)
    for (x, y, w, h) in face_rectangle:
        cv2.rectangle(face_img, (x, y), (x + w, y + h), (255, 255, 255), 5)
        face = img[y:y+h, x:x+w]
        eyes_rectangle = eye_cascade.detectMultiScale(face)
        for (xx, yy, ww, hh) in eyes_rectangle:
            cv2.rectangle(face_img, (xx+x, y+yy), (x+xx + ww, y+yy + hh), (255, 0, 0), 2)

    return face_img


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = detect_face(frame)
    cv2.imshow('face detect', frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()

"""
# opening the camera and capturing a video and saving it in the drive

# Capturing the video from the camera
cap = cv2.VideoCapture(0)

# width and height of the frame
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

output = cv2.VideoWriter('myvideo.mkv',
                         cv2.VideoWriter_fourcc(*'XVID'),
                         20,
                         (width, height))

while True:
    ret, frame = cap.read()
    output.write(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(5) & 0xFF ==27:
        break

cap.release()
output.release()
cv2.destroyAllWindows()
"""

"""
#to display circle by taking center interactively from the user

def draw_circle(event, x, y, flags, param):

    global center, clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        center=(x,y)
        clicked=False
    if event == cv2.EVENT_LBUTTONUP:
        clicked =True

center =(0,0)
clicked = False

cap= cv2.VideoCapture(0)
cv2.namedWindow('testing')
cv2.setMouseCallback('testing',draw_circle)

while True:
    ret, frame =cap.read()
    if clicked:
        cv2.circle(frame,center=center,radius=50,color=(255,0,255), thickness=3)
    cv2.imshow('frame',frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
"""
