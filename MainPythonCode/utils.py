import cv2
from djitellopy import Tello
import numpy as np


def initializeTello():
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity= 0
    myDrone.left_right_velocity= 0
    myDrone.up_down_velocity= 0
    myDrone.yaw_velocity= 0
    myDrone.speed = 0
    myDrone.direction = 1
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone

def telloGetFrame(myDrone, w=360, h=240):
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, w,h)
    return img

def findFace(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.2,4)

    #CODE TO PREVENT TRACKING MUTLIPLE FACES
    myFaceListC= []
    myFaceListArea = []
    area = 5000 

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cx = x + w//2
        cy = y + h//2
        area = w*h
        myFaceListArea.append(area)
        myFaceListC.append([cx,cy])

    if len(myFaceListArea)!= 0:
        #Find index of largest area, i.e. the closest face to the screen
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]], area

    else:
        return img, [[0,0], 0], area
    
def trackFace(myDrone, info, w, pid, pError, area):
    #PID Controllers
    error=info[0][0] - w//2
    speed = pid[0]*error + pid[1]*(error-pError) 
    speed= int(np.clip(speed, -100, 100))#Make sure the speed stays in the boundaries

    if info[0][0]!=0:
        print("FOUND FACE!")
        myDrone.yaw_velocity=speed
        myDrone.up_down_velocity=0
        if (area > 3600):
            myDrone.for_back_velocity = -25
        elif (area <2700):
            myDrone.for_back_velocity = 25
        else:
            myDrone.for_back_velocity = 0
    else: #Keeps moving in a direction until a finds a face
        myDrone.for_back_velocity= 0
        myDrone.left_right_velocity= 0
        myDrone.yaw_velocity= 20 #Continuously rotates

        if myDrone.get_height() >= 170:  # Max height to avoid over-lift
            myDrone.direction = -1
        elif myDrone.get_height() <= 150:  # Min height to avoid crashing
            myDrone.direction = 1
        
        myDrone.up_down_velocity = myDrone.direction * 20  # Move up or down at a constant speed
        error=0
    
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity, myDrone.for_back_velocity,
                                myDrone.up_down_velocity, myDrone.yaw_velocity)
    return error




