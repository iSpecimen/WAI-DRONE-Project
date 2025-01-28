import cv2
import numpy as np
from djitellopy import Tello
from utils import *

#initalising drone and gargi's utils code
myDrone = initializeTello()

#variables
whT = 320
confThresh = 0.6
#reduce nmsThresh to get less bounding boxes
nmsThresh = 0.3

#extracting the names of the different objects we can detect from the coco file
classesFile = 'coco.names'
classNames = []
f = open(classesFile,'rt')
classNames = f.read().rstrip('\n').split('\n')
f.close()
print(classNames)

#traded better speed for reduced accuracy
modelConfiguration = "yolov3-tiny.cfg"
modelWeights = "yolov3-tiny.weights"

#setting up the network using cv2
net = cv2.dnn.readNetFromDarknet(modelConfiguration,modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

#this function identifies objects and then draws a fun little rectangle round them
def findObjects(outputs, img):
    hT,wT,cT = img.shape
    bbox = []
    classIds = [] 
    confVals = []
    #extracts the info from the list of boxes to identify what object each one is and with what confidence and where
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThresh:
                w,h = int(det[2]*wT) ,int(det[3]*hT)
                x,y = int((det[0]*wT) - w/2), int((det[1]*hT) - h/2)
                bbox.append([x,y,w,h])
                #name of the object
                classIds.append(classId)
                confVals.append(float(confidence))
    #eliminates overlapping bounding boxes
    wantedIndices = cv2.dnn.NMSBoxes(bbox,confVals,confThresh,nmsThresh)
    # draws the bounding boxes
    for i in wantedIndices:
        i = i[0]
        box = bbox[i]
        x,y,w,h = box[0], box[1], box[2], box[3]
        #one corner, other corner, colour, thickness of line
        cv2.rectangle(img, (x,y),(x+w,y+h),(255,0,255),2)
        cv2.putTest(img,f'{classNames[classIds[i]]} {int(confVals[i]*100)}%', (x,y-10), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255,0,255),2)
        #should? go up until it cant see the chair or table anymore
        avoid(classIds[i])
    myDrone.up_down_velocity = 0

#my very logical function
def avoid(objectId):
    if objectId=='chair' or objectId == 'diningtable':
        #tries to avoid an object by going up at 20
        myDrone.up_down_velocity = myDrone.direction * 20



#MAIN CODE
while True:
    #no idea if this works to get the video alas
    img = telloGetFrame(myDrone)
    #effectively just casting 
    blob = cv2.dnn.blobFromImage(img,1/255,(whT,whT),[0,0,0],1,crop=False)
    net.setInput(blob)

    #this sorts through the information from the network to get only the outputs
    layerNames = net.getLayerNames()
    outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
    #myfavfunction ;]]]]
    findObjects(outputs,img)

    #does the little screen where we can see what the drone sees
    cv2.imshow("Image",img)
    #neccessary delay
    cv2.waitKey(1)
