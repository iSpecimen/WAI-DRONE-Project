from utils import *
import cv2
import tensorflow as tf
import numpy as np
import pickle
from keras import models
w,h= 280, 280
pid=[0.5,0.5,0] #kp,kd, and ki
myDrone = initializeTello()
pError=0
startCounter = 0 #For no flight, set it as 1, for flight, set to 0qq Qqqq

imageHeight = 280
imageWidth = 280
batchSize = 32
model = models.load_model("faceModel.keras")
namesFile = open("classNames.pkl", "rb")
classNames = pickle.load(namesFile)
namesFile.close()


while True:
    #FLIGHT
    if startCounter == 0:
       # myDrone.takeoff()
        startCounter=1

    img = telloGetFrame(myDrone, (w,h))
    

    img,info, area= findFace(img)
    #GIVES INFORMATION ABOUT THE CENTRE POINT
    print(info[0][0])

    #Using PID controller
    pError= trackFace(myDrone, info, w, pid, pError, area)

    #Using PID controller
 

    #image = tf.keras.utils.load_img(img, target_size=(imageHeight, imageWidth))
    imageArray = tf.keras.utils.img_to_array(img)
    imageArray = tf.expand_dims(imageArray, 0)
    values = model.predict(imageArray)
    print(imageArray)

    prob = np.argmax(values)
    print(classNames[prob])
    print(values)

    cv2.imshow('Image', img)
    if (cv2.waitKey(1) & 0xFF==ord('q')):
        myDrone.land()
        break

    
