import cv2
import VideoStream as webcam
import numpy as np
import time


print ("OpenCV version : " + cv2.__version__)

cap = webcam.VideoStream(1).start()
#cap = cv2.VideoCapture(0)


print ("Camera opened : " + str(cap.isOpened()))

win_name = 'frame'
want_to_exit = False

## Creation de la fenêtre avant la boucle
cv2.namedWindow(win_name)

retval, frame = cap.read()

h = frame.shape[0]
w = frame.shape[1]
img_result = np.zeros([h, w, 1])

millis = lambda : int (round (time.time() * 1000))

previousTime = 0
deltaTime = 0

counter = 1
time_acc = 0


pos = (int(w / 2), int(h / 2))
end = 0


while (not want_to_exit and cv2.getWindowProperty(win_name, 0) >= 0 ):
    currentTime = millis()
    deltaTime = currentTime - previousTime
    previousTime = currentTime
    
    retval, frame = cap.read()

    time_acc += deltaTime

    # Formes
    cv2.ellipse(frame, pos, (100, 100), 0, 0, end, (0, 0, 255))
    cv2.rectangle(frame, (10, 10), (50, 100), (0, 200, 0), -1)

    if (counter >= 30 ):
        counter = 0
        end = (end + 5) % 360
        avg  =  time_acc / 30.0
        time_acc = 0

        print ( " Average per cycle : {:.2f}".format(avg))

    counter += 1
    
    cv2.imshow(win_name, frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        want_to_exit = True
    
cv2.destroyAllWindows()
cap.release()
