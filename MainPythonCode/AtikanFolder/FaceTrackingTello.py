from utils import *
import cv2

w,h= 360, 240
pid=[0.5,0.5,0] #kp,kd, and ki
myDrone = initializeTello()
pError=0
startCounter = 0 #For no flight, set it as 1, for flight, set to 0
track= True
trackbody= False

def get_keyboard_input():
    lr, fb, ud, yaw = 0, 0, 0, 0  # Left/Right, Forward/Backward, Up/Down, Rotate
    speed = 80  # Speed of movement
    keyinput = False

    key = cv2.waitKey(1) & 0xFF
    if key == -1:
        return None
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
    else:
        return None
    
    return None

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
        pError= trackFB(myDrone, info, w, pid, pError, area)
    # if detectThumbsUp(img):
    #     myDrone.rotate_clockwise(180)


    cv2.imshow('Drone View', img)

    # Get manual keyboard input
    control_command = get_keyboard_input()
    if control_command == "quit":
        break  # Exit loop if 'q' is pressed

    # CONTINGENCY STUFF FOR PRESENTATION 
myDrone.land()
cv2.destroyAllWindows()
