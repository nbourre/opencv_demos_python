import cv2
import WebcamVideoStream as webcam
import sys
import time
from matplotlib import pyplot as plt
import numpy as np

print ("OpenCV version : " + cv2.__version__)

def hist_curve(im):
    h = np.zeros((300,256,3))
    if len(im.shape) == 2:
        color = [(255,255,255)]
    elif im.shape[2] == 3:
        color = [ (255,0,0),(0,255,0),(0,0,255) ]
    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([im],[ch],None,[256],[0,256])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        pts = np.int32(np.column_stack((bins,hist)))
        cv2.polylines(h,[pts],False,col)
    y=np.flipud(h)
    return y


cap = webcam.VideoStream(sys.argv[1]).start()
#cap = cv2.VideoCapture(0)


print ("Camera opened : " + str(cap.isOpened()))

if not cap.isOpened():
    print("Capture device error! Args : --> " + sys.argv[1])
    sys.exit(0)

win_name = 'frame'
win_roi = 'roi'
win_roi_2 = 'roi_2'
win_hue = "Hue"
win_sat = 'Saturation'
win_val = 'Value'

want_to_exit = False

## Creation de la fenêtre avant la boucle
cv2.namedWindow(win_name)

retval, frame = cap.read()

img_height = frame.shape[0]
img_width = frame.shape[1]

left_roi = int(img_width / 5) * 2
right_roi = img_width - left_roi
top_roi = int(img_height / 9) * 4
bottom_roi = img_height - top_roi

num_pixels = (right_roi - left_roi) * (bottom_roi - top_roi)

bins = np.arange(256).reshape(256,1)

millis = lambda : int (round (time.time() * 1000))

previousTime = 0
deltaTime = 0

counter = 1
time_acc = 0
pause = False

while (not want_to_exit and cv2.getWindowProperty(win_name, 0) >= 0 ):

    ## Gestion de temps
    currentTime = millis()
    deltaTime = currentTime - previousTime
    previousTime = currentTime
    
    time_acc += deltaTime

    if (not pause):
        ## Gestion de la lecture
        retval, frame = cap.read()


        ## Pipeline
        
        # ROI
        roi = frame[:, left_roi:right_roi]
        roi_2 = frame[top_roi:bottom_roi, left_roi:right_roi]

        img_hue, img_sat, img_val = cv2.split (cv2.cvtColor(roi_2, cv2.COLOR_BGR2HSV))

        im = img_hue

        img_histo = np.zeros((300,256,3))

        if len(im.shape) == 2:
            color = [(255,255,255)]
        elif im.shape[2] == 3:
            color = [ (255,0,0),(0,255,0),(0,0,255) ]

        # enumerate retourne l'index avec l'énumérateur
        for ch, col in enumerate(color):
            hist_item = cv2.calcHist([im],[ch],None,[256],[0,256])

            # Récupérer la valeur maximum
            hist_max = np.amax(hist_item)
            hist_max_idx = np.argmax(hist_item)

            # Normalisation pour caper à 255
            cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)

            # Arrondi et cast les valeurs
            hist=np.int32(np.around(hist_item))

            # Creation de la matrice de points
            pts = np.int32(np.column_stack((bins,hist)))

            # Traçage de l'histrogramme avec les points
            cv2.polylines(img_histo,[pts],False,col)

        # flip l'image
        img_histo=np.flipud(img_histo)
        

        ## Affichage et autres sorties
        if (counter >= 30 ):
            counter = 0
            avg  =  time_acc / 30.0
            time_acc = 0

            print ( " Average per cycle : " + str (avg))

        counter += 1
    
    cv2.imshow(win_name, frame)
    #cv2.imshow(win_roi, roi)
    cv2.imshow(win_roi_2, roi_2)
    cv2.imshow(win_hue, img_histo)

    
    ## Gestion des entrées
    key_val = cv2.waitKey(1) & 0xFF
    if key_val == 27:
        want_to_exit = True
    if key_val == ord(' '):
        pause = not pause

    
cv2.destroyAllWindows()
cap.release()
