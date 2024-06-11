#!./env/bin/python3
import cv2

# open camera
cap = cv2.VideoCapture('/dev/ttyAMA10', cv2.CAP_ANY)
# set dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
# take frame
ret, frame = cap.read()
# write frame to file
# cv2.imwrite('image.jpg', frame)
# release camera
cap.release()
