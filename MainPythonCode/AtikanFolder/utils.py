import cv2
from djitellopy import Tello
import numpy as np
import mediapipe as mp

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
    area = 0

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

# def findBody(img):
#     faceCascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
#     imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#     bodies = faceCascade.detectMultiScale(imgGray,1.2,4)
    
#     myBodyListC = []
#     myBodyListArea = []
#     area = 0
    
#     for (x, y, w, h) in bodies:
#         cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#         cx = x + w // 2
#         cy = y + h // 2
#         area = w * h
#         myBodyListArea.append(area)
#         myBodyListC.append([cx, cy])
#     if len(myBodyListArea)!=0:

#         i = myBodyListArea.index(max(myBodyListArea))
#         return img, [myBodyListC[i], myBodyListArea[i]], area
#     else:
#         return img, [[0,0], 0], area
    
def trackFB(myDrone, info, w, pid, pError, area):
    #PID Controllers
    error=info[0][0] - w//2
    speed = pid[0]*error + pid[1]*(error-pError) 
    speed= int(np.clip(speed, -100, 100))#Make sure the speed stays in the boundaries

    if info[0][0]!=0:
        print("FOUND TRACK!")
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
        myDrone.yaw_velocity= 25 #Continuously rotates

        if myDrone.get_height() >= 160:  # Max height to avoid over-lift
            myDrone.direction = -1
        elif myDrone.get_height() <= 140 :  # Min height to avoid crashing
            myDrone.direction = 1
        
        myDrone.up_down_velocity = myDrone.direction * 20  # Move up or down at a constant speed
        error=0
    
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity, myDrone.for_back_velocity,
                                myDrone.up_down_velocity, myDrone.yaw_velocity)
    return error

    
def detectThumbsUp(img):
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            thumb_tip = handLms.landmark[mpHands.HandLandmark.THUMB_TIP]
            thumb_ip = handLms.landmark[mpHands.HandLandmark.THUMB_IP]
            index_mcp = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP]
            
            if thumb_tip.y < thumb_ip.y < index_mcp.y:
                return True
    return False