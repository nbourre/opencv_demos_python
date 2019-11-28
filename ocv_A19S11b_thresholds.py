import cv2

print ("OpenCV version : " + cv2.__version__)

cap = cv2.VideoCapture(1)

print ("Camera opened : " + str(cap.isOpened()))

win_name = 'frame'
win_binary = 'Binary threshold'

thresh_val = 127
pix_max = 255

want_to_exit = False

key_val = 0
inc_value = 3

## Creation de la fenêtre avant la boucle
cv2.namedWindow(win_name)

while (not want_to_exit and cv2.getWindowProperty(win_name, 0) >= 0 ):
    ret, frame = cap.read()
    
    couche_b, couche_g, couche_r = cv2.split(frame)

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
    
    ret_thresh, img_binary = cv2.threshold(couche_r, thresh_val, pix_max, cv2.THRESH_BINARY)


    cv2.imshow(win_name, frame)
    cv2.imshow(win_binary, img_binary)
    
    key_val = cv2.waitKey(1) & 0xFF

    if  key_val == 27:
        want_to_exit = True
    elif key_val == ord('=') or key_val == ord('+'):
        thresh_val = min (255, thresh_val + inc_value)
        print ('thresh_val = ' + str(thresh_val))
    elif key_val == ord('-'):
        thresh_val = max (0, thresh_val - inc_value)
        print ('thresh_val = ' + str(thresh_val))
    
cv2.destroyAllWindows()
cap.release()