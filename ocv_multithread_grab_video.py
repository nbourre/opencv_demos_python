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
want_to_exit = False

## Creation de la fenêtre avant la boucle
cv2.namedWindow(win_name)

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

    ## Affichage et autres sorties
    if (counter >= 30 ):
        counter = 0
        avg  =  time_acc / 30.0
        time_acc = 0

        print ( " Average per cycle : " + str (avg))

    counter += 1
    
    cv2.imshow(win_name, frame)
    
    ## Gestion des entrées
    key_val = cv2.waitKey(1) & 0xFF
    if key_val == 27:
        want_to_exit = True

    
cv2.destroyAllWindows()
cap.release()
