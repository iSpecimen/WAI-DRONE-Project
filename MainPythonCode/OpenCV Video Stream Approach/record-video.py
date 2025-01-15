import time, cv2
from threading import Thread
from djitellopy import Tello

tello = Tello()

tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()
timestamp = time.strftime("%Y-%m-%d")

def videoRecorder():
    # create a VideoWrite object, recoring to ./videostream.avi
    height, width, _ = frame_read.frame.shape
    print("Height:", height, " || Width:", width)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter('videostream.avi', fourcc, 30, (width, height))
    print("Started Recording.")

    while keepRecording:
        frame = frame_read.frame #
        #If it can::
        """
        Can the frame above be used as an image??
        If it can then using the compiled model and a function either in this file or saved as a separate file
        call loadModel(frame), depending on how many classes we do the output should be an array with the probabilities
        of each class, then use np argmax to get the highest then call some other functions depending on outcome
        """
        if frame is not None:
            video.write(frame)
        else:
            print("Warning: Frame is None!")
        time.sleep(1 / 30)

    video.release()
    print("Stopped video recording now.")

# we need to run the recorder in a seperate thread, otherwise blocking options
#  would prevent frames from getting added to the video
recorder = Thread(target=videoRecorder)
recorder.start()

print("Current Battery Level:", tello.get_battery())
# tello.takeoff()
print("Waiting 10 seconds.")
time.sleep(10)
print("Waiting over")
# tello.move_up(100)
# time.sleep(1000)
# tello.rotate_counter_clockwise(360)
# time.sleep(1000)
# tello.land()

keepRecording = False
recorder.join()

try:
    tello.streamoff()
except Exception as e:
    print(f"Error turning off stream: {e}")
