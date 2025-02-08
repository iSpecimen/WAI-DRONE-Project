from utils import *
import cv2

w,h= 360, 240
pid=[0.5,0.5,0] #kp,kd, and ki
myDrone = initializeTello()
pError, pError_ud= 0, 0

startCounter = 0 #For no flight, set it as 1, for flight, set to 0
track= True
trackbody= False



while True:
    #FLIGHT
    if startCounter == 0:
        myDrone.takeoff()
        startCounter=1
    print("Battery Level: " ,  myDrone.get_battery())
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
        pError, pError_ud= trackFB(myDrone, info, w, h, pid, pError, pError_ud, area)
    # if detectThumbsUp(img):
    #     myDrone.rotate_clockwise(180)


    cv2.imshow('Drone View', img)

    # # Get manual keyboard input
    # control_command = get_keyboard_input()
    # if control_command == "quit":
    #     break  # Exit loop if 'q' is pressed

    # CONTINGENCY STUFF FOR PRESENTATION 
myDrone.land()
cv2.destroyAllWindows()
