import cv2
import numpy as np
import matplotlib.pyplot as plt

#%matplotlib inline

face_cascade = cv2.CascadeClassifier(r"F:\Project_Data\haarcascade_frontalface_default.xml")
eye_cascade=cv2.CascadeClassifier(r"F:\Project_Data\haarcascade_eye.xml")

def detect_face(img):
    face_img=img.copy()
    face_rectangle = face_cascade.detectMultiScale(face_img)
    xt=yt=yb=xb=0
    for (x,y,w,h) in face_rectangle:
        xt=x
        yt=y
        xb=x+w
        yb=y+h
        cv2.rectangle(face_img,(x,y),(x+w,y+h),(255,255,255),5)
        break
    eyes_rectangle = eye_cascade.detectMultiScale(face_img)
    for (x,y,w,h) in eyes_rectangle:
        if x>=xt and y>=yt and x<=xb and y<=yb and x+w<=xb and y+h<=yb:
            cv2.rectangle(face_img, (x, y), (x + w, y + h), (255, 0, 0), 5)
        break
    return face_img

cap= cv2.VideoCapture(0)

while True:
    ret, frame =cap.read()
    frame = detect_face(frame)
    cv2.imshow('face detect', frame)
    if cv2.waitKey(5) & 0xFF ==27:
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
