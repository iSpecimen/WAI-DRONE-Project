import cv2
#change variables
sensitivity = 120

#read video
video_path = "C:/Users/jessi/Pictures/Camera Roll/WIN_20241114_18_18_33_Pro.mp4"

video = cv2.VideoCapture(video_path)

#visualize video??
frameready = True
while frameready:
    frameready, frame = video.read()
    if frameready:
        #using thresholding to seperate person from background
        #gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #ret, thresholding = cv2.threshold(gray_scale,sensitivity,255,cv2.THRESH_BINARY)
        #cv2.imshow('frame',thresholding)
        edger = cv2.Canny(frame, 100,300)
        #each contour is an isolated area of white in the frame
        contours, hierarchy = cv2.findContours(edger, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:            
            areaval = cv2.contourArea(cnt)
            if areaval > 20:
                print(areaval)

        cv2.imshow('frame', edger)
        #the no is the inverse of the frame rate in milliseconds
        cv2.waitKey(33)
video.release()
cv2.destroyAllWindows()