import cv2
import numpy as np

#need to replace with the drone video
cap = cv2.VideoCapture(0)

classesFile = 'coco.names'
classNames = []
f = open(classesFile,'rt')
classNames = f.read().rstrip('\n').split('\n')
f.close()
print(classNames)

while True:
    success, img = cap.read()
    cv2.imshow("Image",img)
    cv2.waitKey(1)
