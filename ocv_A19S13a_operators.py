import cv2
import WebcamVideoStream as webcam
import sys
import time


print ("OpenCV version : " + cv2.__version__)


cap = webcam.VideoStream(sys.argv[1]).start()


#cap = cv2.VideoCapture(0)


print ("Camera opened : " + str(cap.isOpened()))

if not cap.isOpened():
    print("Capture device error! Args : --> " + sys.argv[1])
    sys.exit(0)

win_name = 'frame'
win_roi = 'roi'
win_roi_2 = 'roi_2'
win_template = 'template'
win_diff = 'Difference'

want_to_exit = False

## Creation de la fenêtre avant la boucle
cv2.namedWindow(win_name)

retval, frame = cap.read()

if (len(sys.argv) > 2):
    template = cv2.imread(sys.argv[2], 0)
    if (template is None):
        print ("Unable to load " + sys.argv[2])
        template = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
else :
    template = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)

img_height = frame.shape[0]
img_width = frame.shape[1]

left_roi = int(img_width / 5) * 2
right_roi = img_width - left_roi
top_roi = int(img_height / 5) * 2
bottom_roi = img_height - top_roi

millis = lambda : int (round (time.time() * 1000))

previousTime = 0
deltaTime = 0

counter = 1
time_acc = 0

while (not want_to_exit and cv2.getWindowProperty(win_name, 0) >= 0 ):

    ## Gestion de temps
    currentTime = millis()
    deltaTime = currentTime - previousTime
    previousTime = currentTime
    
    time_acc += deltaTime

    ## Gestion de la lecture
    retval, frame = cap.read()


    ## Pipeline
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_diff = cv2.absdiff(img_gray, template)
    
    
    # ROI
    roi = img_diff[:, left_roi:right_roi]
    roi_2 = img_diff[top_roi:bottom_roi, left_roi:right_roi]

    #cv2.rectangle(frame, (left_roi, top_roi), (left_roi + (right_roi - left_roi), top_roi + (bottom_roi - top_roi)), (0, 255, 0), 2)

    ## Affichage et autres sorties
    if (counter >= 30 ):
        counter = 0
        avg  =  time_acc / 30.0
        time_acc = 0

        print ( " Average per cycle : " + str (avg))

    counter += 1
    
    cv2.imshow(win_name, frame)
    cv2.imshow(win_roi, roi)
    cv2.imshow(win_roi_2, roi_2)

    cv2.imshow(win_template, template)
    cv2.imshow(win_diff, img_diff)
    
    ## Gestion des entrées
    key_val = cv2.waitKey(1) & 0xFF
    if key_val == 27:
        want_to_exit = True

    
cv2.destroyAllWindows()
cap.release()
