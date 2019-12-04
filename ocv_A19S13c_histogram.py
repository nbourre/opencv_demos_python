import cv2
import VideoStream as webcam
import sys
import time
from matplotlib import pyplot as plt
import numpy as np

print ("OpenCV version : " + cv2.__version__)

def rmse(predictions, targets):
    """
    Retourne la racine de l'erreur quadratique moyenne
    entre deux vecteurs de même dimension
    """
    differences = predictions - targets                       #the DIFFERENCEs.
    differences_squared = differences ** 2                    #the SQUAREs of ^
    mean_of_differences_squared = differences_squared.mean()  #the MEAN of ^
    rmse_val = np.sqrt(mean_of_differences_squared)           #ROOT of ^
    return rmse_val                                           #get the ^


def hist_curve(im):
    """
    Retourne l'image de l'histogramme, le vecteur de l'histogramme,
    la valeur maximum et l'index de la valeur maximum
    """
    h = np.zeros((300,256,3))

    if len(im.shape) == 2:
        color = [(255,255,255)]
    elif im.shape[2] == 3:
        color = [ (255,0,0),(0,255,0),(0,0,255) ]

    # enumerate retourne l'index avec l'énumérateur
    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([im],[ch],None,[256],[0,256])

        # Normalisation pour caper à 255
        cv2.normalize(hist_item, hist_item, 0, 255, cv2.NORM_MINMAX)

        # Arrondi et cast les valeurs
        hist=np.int32(np.around(hist_item))

        # Creation de la matrice de points
        pts = np.int32(np.column_stack((bins,hist)))

        # Traçage de l'histrogramme avec les points
        cv2.polylines(h,[pts],False,col)

        # Récupérer la valeur maximum
        hist_max = np.amax(hist_item)
        hist_max_idx = np.argmax(hist_item)
    
    out = np.flipud(h)
    h = None
    return out, hist_item, hist_max, hist_max_idx



if len(sys.argv) > 1 :
    src = sys.argv[1]
else:
    src = 1 ## Change here if you want to use your camera

cap = webcam.VideoStream(src).start()


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
top_roi = int(img_height / 11) * 5
bottom_roi = img_height - top_roi

num_pixels = (right_roi - left_roi) * (bottom_roi - top_roi)

bins = np.arange(256).reshape(256,1)

millis = lambda : int (round (time.time() * 1000))

previousTime = 0
deltaTime = 0

counter = 1
time_acc = 0
pause = False

## Truc de texte
font = cv2.FONT_HERSHEY_SIMPLEX
txt_left = 10
txt_top = img_height - 40
txt_scale = 1
txt_color = (255, 255, 255)
txt_thickness = 2

save_template = False

img_histo = np.zeros((300,256,3), np.uint8)

template_img = None
template_hist = None

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
        # Remise à zéro de l'histogramme
        img_histo = img_histo * 0

        # ROI
        roi = frame[:, left_roi:right_roi]
        roi_2 = frame[top_roi:bottom_roi, left_roi:right_roi]

        img_hue, img_sat, img_val = cv2.split (cv2.cvtColor(roi_2, cv2.COLOR_BGR2HSV))

        im = img_hue
       
        img_histo, img_histo_items, hist_max, hist_max_idx = hist_curve(im)

        if save_template :
            template_img = roi_2.copy()
            template_h, template_s, template_v = cv2.split (cv2.cvtColor(template_img, cv2.COLOR_BGR2HSV))
            template_hist, template_hist_items, template_max, template_max_idx = hist_curve(template_h)
            cv2.imshow("Template", template_img)
            save_template = False

        # Textes
        txt = "End : " + str(hist_max_idx)
        size, baseline = cv2.getTextSize(txt, font, txt_scale, txt_thickness)
        baseline += txt_thickness
        txt_width = size[0]
        txt_height = size[1]

        txt_orig = (img_histo.shape[1] - (txt_width + 10), img_histo.shape[0] - 40)
        
        # Why it works??? Might me because img_histo is read-only
        # Src : https://stackoverflow.com/questions/36042508/opencv-puttext-in-python-error-after-array-manipulation
        img_histo_output = img_histo.copy()

        cv2.putText(img_histo_output, txt, txt_orig, font, txt_scale, txt_color, txt_thickness, cv2.LINE_AA)

        
        if template_img is not None :
            compare_start = 0
            compare_end = 45
            template_error = rmse(template_hist_items[compare_start:compare_end], img_histo_items[compare_start:compare_end])

            # test
            if template_error < 50:
                cv2.imshow("Good enough", roi_2)

        ## Affichage et autres sorties
        if (counter >= 30 ):
            counter = 0
            avg  =  time_acc / 30.0
            time_acc = 0

            if template_img is not None :
                print ("Erreur : " + str(template_error))

        counter += 1
    
    cv2.imshow(win_name, frame)
    #cv2.imshow(win_roi, roi)
    cv2.imshow(win_roi_2, roi_2)
    cv2.imshow(win_hue, img_histo_output)

    
    ## Gestion des entrées
    key_val = cv2.waitKey(1) & 0xFF
    if key_val == 27:
        want_to_exit = True
    if key_val == ord(' '):
        pause = not pause
        cap.pause = pause
        print ("Erreur (pause): " + str(template_error))
    if key_val == ord('z'):
        cap.delay = max(0, cap.delay - 1)
        print ("Capture delay = " + str (cap.delay))
    if key_val == ord('x'):
        cap.delay = cap.delay + 1
        print ("Capture delay = " + str (cap.delay))
    if key_val == ord('c'):
        template_error = sys.maxsize
        save_template = True

    
cv2.destroyAllWindows()
cap.release()
