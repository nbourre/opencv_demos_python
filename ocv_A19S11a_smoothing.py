import cv2

print ("OpenCV version : " + cv2.__version__)

cap = cv2.VideoCapture(0) #On my work laptop

print ("Camera opened : " + str(cap.isOpened()))

win_name = 'frame'
win_blur = 'average blur'
win_median = 'median blur'
win_gaussian = 'gaussian blur'

want_to_exit = False

kernel_size = (7, 7)

## Creation de la fenêtre avant la boucle
cv2.namedWindow(win_name)

while (not want_to_exit and cv2.getWindowProperty(win_name, 0) >= 0 ):
    ret, frame = cap.read()
    
    img_blur = cv2.blur(frame, kernel_size)
    img_median = cv2.medianBlur(frame, kernel_size[0])
    img_gaussian = cv2.GaussianBlur(frame, kernel_size, kernel_size[0]/3.0) #SigmaX <-- Distance en pixel du centre



    cv2.imshow(win_name, frame)
    cv2.imshow(win_blur, img_blur)
    cv2.imshow(win_median, img_median)
    cv2.imshow(win_gaussian, img_gaussian)
    
    if cv2.waitKey(1) & 0xFF == 27:
        want_to_exit = True
    
cv2.destroyAllWindows()
cap.release()