import cv2
import numpy as np
import WebcamVideoStream as webcam

cap = webcam.VideoStream(1).start()

kernel = np.ones((5, 5), np.uint8)
iterations = 1

# define range of blue color in HSV
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])


while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv)
    blurred = cv2.blur(h, (5, 5))

    hsv = cv2.merge([h, s, v])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.dilate(mask, kernel, iterations=iterations)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    key_val = cv2.waitKey(5) & 0xFF
    if key_val == 27:
        break
    if (key_val == ord('+') or key_val == ord('=')):
        dirty_data = True
        iterations = min(5, iterations + 1)
    if (key_val == ord('-')):
        dirty_data = True
        iterations = max(1, iterations - 1)

cv2.destroyAllWindows()
cap.release()