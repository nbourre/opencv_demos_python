import cv2
import WebcamVideoStream as webcam
import sys
import time
import numpy as np

display_fps = False

print ("OpenCV version : " + cv2.__version__)


cap = webcam.VideoStream(1).start()


#cap = cv2.VideoCapture(0)


print ("Camera opened : " + str(cap.isOpened()))

if not cap.isOpened():
    print("Capture device error! Args : --> " + sys.argv[1])
    sys.exit(0)

win_name = 'frame'
win_roi = 'roi'
win_roi_2 = 'roi_2'
win_gray = 'gray'
win_thresh = 'Threshold'

want_to_exit = False

## Creation de la fenêtre avant la boucle
cv2.namedWindow(win_name)

retval, frame = cap.read()

if len(sys.argv) > 2 :
    template = cv2.imread(sys.argv[2], 0)
    if template is None :
        print ("Unable to load " + sys.argv[2])
        template = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
else :
    template = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)

img_height = frame.shape[0]
img_width = frame.shape[1]

left_roi = (img_width // 5) * 2
right_roi = img_width - left_roi
top_roi = (img_height // 5) * 2
bottom_roi = img_height - top_roi

millis = lambda : int (round (time.time() * 1000))

previousTime = 0
deltaTime = 0

counter = 1
time_acc = 0

thresh_val = 199
inc_value = 2

reducing_factor = 4

img_small_dim = (img_height // reducing_factor, img_width // reducing_factor)

while not want_to_exit and cv2.getWindowProperty(win_name, 0) >= 0:

    ## Gestion de temps
    currentTime = millis()
    deltaTime = currentTime - previousTime
    previousTime = currentTime
    
    time_acc += deltaTime

    ## Gestion de la lecture
    retval, frame = cap.read()
    img_small = cv2.resize(frame, img_small_dim)
    img_gray = cv2.cvtColor(img_small, cv2.COLOR_BGR2GRAY)
    
    ## Pipeline
    retVal, img_thresh = cv2.threshold(img_gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
    img_temp, contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rescaled_contours = [np.multiply(contour, reducing_factor) for contour in contours]

    # Trace tous les contours
    img_outputA = cv2.drawContours(img_outputA, rescaled_contours, -1, (0,255,0), 1)

    # Trace que le 4e contour
    cnt = rescaled_contours[3]
    img_outputB = cv2.drawContours(img_outputB, cnt, 0, (255,255,0), 2)

    ## Affichage et autres sorties
    if counter >= 30:
        counter = 0
        avg = time_acc / 30.0
        time_acc = 0

        if display_fps:
            print(" Average per cycle : " + str(avg))

    counter += 1
    
    cv2.imshow(win_name, frame)
    cv2.imshow(win_gray, img_gray)
    cv2.imshow(win_thresh, img_thresh)
    cv2.imshow("Output A", img_outputA)
    cv2.imshow("Output B", img_outputB)

    ## Gestion des entrées
    key_val = cv2.waitKey(1) & 0xFF

    if key_val == 27:
        want_to_exit = True
    elif key_val == ord('=') or key_val == ord('+'):
        thresh_val = min (255, thresh_val + inc_value)
        print ('thresh_val = ' + str(thresh_val))
    elif key_val == ord('-'):
        thresh_val = max (0, thresh_val - inc_value)
        print ('thresh_val = ' + str(thresh_val))

    
cv2.destroyAllWindows()
cap.release()
