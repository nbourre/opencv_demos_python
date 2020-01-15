import cv2
import VideoStream as webcam

import time


print ("OpenCV version : " + cv2.__version__)

cap = webcam.VideoStream(src=0).start()
#cap = cv2.VideoCapture(0)


print ("Camera opened : " + str(cap.isOpened()))

win_name = 'frame'
win_hue = "Hue - Teinte"
win_sat = "Saturation"
win_val = "Value - Valeur"
win_gray = "Gray values - Niveaux de gris"

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
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    img_h, img_s, img_v = cv2.split(img_hsv)


    ## Affichage et autres sorties
    if (counter >= 30 ):
        counter = 0
        avg  =  time_acc / 30.0
        time_acc = 0

        print ( " Average per cycle : " + str (avg))

    counter += 1
    
    cv2.imshow(win_name, frame)
    cv2.imshow(win_hue, img_h)
    cv2.imshow(win_sat, img_s)
    cv2.imshow(win_val, img_v)
    cv2.imshow(win_gray, img_gray)
    
    ## Gestion des entrées
    key_val = cv2.waitKey(1) & 0xFF
    if key_val == 27:
        want_to_exit = True

    
cv2.destroyAllWindows()
cap.release()
