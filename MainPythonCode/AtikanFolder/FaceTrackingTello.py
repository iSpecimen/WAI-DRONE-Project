from utils import *
import cv2

w,h= 360, 240
pid=[0.5,0.5,0] #kp,kd, and ki
myDrone = initializeTello()
pError=0
startCounter = 0#For no flight, set it as 1, for flight, set to 0
track= True
trackbody= False

while True:
    #FLIGHT
    if startCounter == 0:
        myDrone.takeoff()
        startCounter=1

    img = telloGetFrame(myDrone, (w,h))
    img,info, area= findFace(img)
    # if area != 0:
    #     trackbody = True
    # if trackbody:
    #     img,info, area = findBody(img)
    #GIVES INFORMATION ABOUT THE CENTRE POINT
    print(info[0][0])

    #Using PID controller
    if track:
        pError= trackFB(myDrone, info, w, pid, pError, area)
    if detectThumbsUp(img):
        myDrone.rotate_clockwise(180)


    cv2.imshow('Drone View', img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        myDrone.land()
        break
