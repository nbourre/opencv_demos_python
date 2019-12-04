import os
import cv2
import VideoStream as webcam
import sys
import time


print ("OpenCV version : " + cv2.__version__)

filename = sys.argv[1]
folder = os.path.dirname(filename)

cap = webcam.VideoStream(1).start()
#cap = cv2.VideoCapture(0)


print ("Camera opened : " + str(cap.isOpened()))

if not cap.isOpened():
    print("Capture device error! Args : --> " + filename)
    sys.exit(0)

win_name = 'frame'
win_thresh = 'threshold'
win_gray = 'gray'

want_to_exit = False

create_mask = False
thresh = 127

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

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    retVal, img_thresh = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)

    ## Pipeline
    if (create_mask):
        create_mask = False
        

        ## Python does not like spaces in filenames when saving...

        #output_file = 'mask_' + str(currentTime) + '.jpg'
        #output_file = os.path.join(folder, output_file)
        output_file = r'c:\temp\mask_' + str(currentTime) + ".jpg"

        print('Capturing mask --> ' + output_file)
        if not cv2.imwrite(output_file, img_thresh):
            raise Exception('Could not write image')


    ## Affichage et autres sorties
    if (counter >= 30 ):
        counter = 0
        avg  =  time_acc / 30.0
        time_acc = 0

        ##print ( " Average per cycle : " + str (avg))

    counter += 1
    
    cv2.imshow(win_name, frame)
    cv2.imshow(win_thresh, img_thresh)
    cv2.imshow(win_gray, img_gray)
    
    ## Gestion des entrées
    key_val = cv2.waitKey(1) & 0xFF
    if key_val == 27:
        want_to_exit = True
    if key_val == ord('c'):
        
        create_mask = True
    if key_val == ord('-'):
        thresh = max(1, thresh - 1)
    if key_val == ord('+') or key_val == ord('=') :
        thresh = min(255, thresh + 1)
    
cv2.destroyAllWindows()
cap.release()
