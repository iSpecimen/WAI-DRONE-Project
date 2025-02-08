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
    
def get_keyboard_input(myDrone):
    lr, fb, ud, yaw = 0, 0, 0, 0  # Left/Right, Forward/Backward, Up/Down, Rotate
    speed = 80  # Speed of movement
    keyinput = False

    key = cv2.waitKey(1) & 0xFF
 
    if key == ord('q'):  # Quit and land
        myDrone.land()
        return "quit"

    if key == ord('w'):
        fb = speed
        keyinput=True
    elif key == ord('s'):
        fb = -speed
        keyinput=True

    if key == ord('j'):  # Left (Left Arrow)
        lr = -speed
        keyinput=True
    elif key == ord('l'):  # Right (Right Arrow)
        lr = speed
        keyinput=True

    if key == ord('i'):  # Up
        ud = speed
        keyinput=True
    elif key == ord('k'):  # Down
        ud = -speed
        keyinput=True

    if key == ord('a'):  # Rotate Left
        yaw = -speed
        keyinput=True
    elif key == ord('d'):  # Rotate Right
        yaw = speed
        keyinput=True
    if keyinput:
        myDrone.send_rc_control(lr, fb, ud, yaw)
        keyinput=False
    else:
        keyinput= False
        return "No Input"
    return None

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
    
def trackFB(myDrone, info, w, h, pd, pError, pError_ud, area):
    foundface=False
    #PD Controllers (Proportional Derivative Controller)
    error=info[0][0] - w//2
    speed = pd[0]*error + pd[1]*(error-pError) #pError is previous error, calculate change in error to know the rate of change of error.
    speed= int(np.clip(speed, -100, 100)) #Make sure the speed stays in the boundaries

    # --- Up/Down Movement (PD Controller) ---
    error_ud = info[0][1] - h//2 
    speed_ud = pd[0] * error_ud + pd[1] * (error_ud - pError_ud)
    speed_ud = int(np.clip(speed_ud, -90, 90))  # Limit altitude speed

    if info[0][0]!=0:
        print("FOUND TRACK! (Ensure Safe distance movement)")
        foundface=True
        myDrone.yaw_velocity=speed
        myDrone.up_down_velocity=-speed_ud
        if (area > 3300):
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
        if get_keyboard_input(myDrone) == "No Input":
            myDrone.send_rc_control(myDrone.left_right_velocity, myDrone.for_back_velocity, myDrone.up_down_velocity, myDrone.yaw_velocity)
    return error, error_ud

    
# def detectThumbsUp(img):
#     mpHands = mp.solutions.hands
#     hands = mpHands.Hands()
#     mpDraw = mp.solutions.drawing_utils
#     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(imgRGB)
    
#     if results.multi_hand_landmarks:
#         for handLms in results.multi_hand_landmarks:
#             thumb_tip = handLms.landmark[mpHands.HandLandmark.THUMB_TIP]
#             thumb_ip = handLms.landmark[mpHands.HandLandmark.THUMB_IP]
#             index_mcp = handLms.landmark[mpHands.HandLandmark.INDEX_FINGER_MCP]
            
#             if thumb_tip.y < thumb_ip.y < index_mcp.y:
#                 return True
#     return False