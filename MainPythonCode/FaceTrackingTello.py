from utils import *
import cv2

w,h= 360, 240
pid=[0.5,0.5,0] #kp,kd, and ki
myDrone = initializeTello()
pError=0
startCounter = 0 #For no flight, set it as 1, for flight, set to 0qq Qqqq

while True:
    #FLIGHT
    if startCounter == 0:
        myDrone.takeoff()
        startCounter=1

    img = telloGetFrame(myDrone, (w,h))
    img,info, area= findFace(img)
    #GIVES INFORMATION ABOUT THE CENTRE POINT
    print(info[0][0])

    #Using PID controller
    pError= trackFace(myDrone, info, w, pid, pError, area)

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        myDrone.land()
        break
