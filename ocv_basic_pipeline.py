import sys
import cv2
import WebcamVideoStream as webcam

import time


print ("OpenCV version : " + cv2.__version__)

is_camera = len(sys.argv) == 1

if (is_camera) :
    cap = webcam.WebcamVideoStream(1).start()
    retval, frame = cap.read()
else :
    frame = cv2.imread(sys.argv[1])

win_main = "Originale"
win_median = "Median"
win_gray = "Niveaux de gris"

key_val = 0
want_to_exit = False
dirty_flag = True
blur_val = 7
inc_value = 2

while (not want_to_exit):
    key_val = cv2.waitKey(1) & 0xFF

    if is_camera :
        retval, frame = cap.read()
        dirty_flag = True
    
    
    if dirty_flag:
        # Conversion
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Analyse
        img_smooth = cv2.medianBlur(img_gray, blur_val)

    
    cv2.imshow(win_main, frame)
    cv2.imshow(win_gray, img_gray)
    cv2.imshow(win_median, img_smooth)


    if  key_val == 27:
        want_to_exit = True
    elif key_val == ord('=') or key_val == ord('+'):
        blur_val = min (255, blur_val + inc_value)
        print ('blur_val = ' + str(blur_val))
        dirty_flag = True
    elif key_val == ord('-'):
        blur_val = max (1, blur_val - inc_value)
        print ('blur_val = ' + str(blur_val))
        dirty_flag = True

if (is_camera):
    cap.release()

cv2.destroyAllWindows()