import cv2
import RPI.GPIO as GPIO

sensor = 4

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 440)

while cv2.waitKey(33) < 0:
    ret, frame = cam.read()
    cv2.imshow("VideoFrame", frame)
    if cam.isOpened():
        print("OPEN")
    else:
        print("NO")

cam.release()
cv2.destroyAllWindows()


