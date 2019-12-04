import cv2
import VideoStream as webcam
import numpy as np
import time


print ("OpenCV version : " + cv2.__version__)

cap = webcam.VideoStream(src=1).start()
#cap = cv2.VideoCapture(0)


print ("Camera opened : " + str(cap.isOpened()))

win_name = 'frame'
win_sobel = 'sobel'
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
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Calcul en X
    sobelx64f = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    abs_sobelx64f = np.absolute(sobelx64f)
    cv2.imshow("text x", cv2.convertScaleAbs(sobelx64f))
    
    # Calcul en Y
    sobely64f = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    abs_sobely64f = np.absolute(sobely64f)
    cv2.imshow("text y", cv2.convertScaleAbs(sobely64f))
    
    # Somme ponderee
    sobel_64f = cv2.addWeighted(abs_sobelx64f, 0.5, abs_sobely64f, 0.5, 0)

    # Conversion en 8 bit
    sobel_8u = np.uint8(sobel_64f)

    ## Affichage et autres sorties
    if (counter >= 30 ):
        counter = 0
        avg  =  time_acc / 30.0
        time_acc = 0

        print ( " Average per cycle : " + str (avg))

    counter += 1
    
    cv2.imshow(win_name, frame)
    cv2.imshow(win_sobel, sobel_8u)

    ## Gestion des entrées
    key_val = cv2.waitKey(1) & 0xFF
    if key_val == 27:
        want_to_exit = True


cv2.destroyAllWindows()
cap.release()
