

import socket
import cv2

# #they won't give it to us, so it's our turn to figure out how to turn the cameras on, on the drone.
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# tello_address = ('192.168.10.1', 8889)  # Drone IP address
# sock.bind(('', 11111))

tello_video = cv2.VideoCapture('udp://@0.0.0.0:11111')

while True:
    try:
        ret, frame = tello_video.read()
        if ret:
            cv2.imshow('Tello', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as err:
        print(err)  
        
tello_video.release()
cv2.destroyAllWindows()
       
        