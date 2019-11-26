import cv2
import WebcamVideoStream as webcam
import sys
import time
from matplotlib import pyplot as plt
import numpy as np

print ("OpenCV version : " + cv2.__version__)


cap = webcam.WebcamVideoStream(sys.argv[1]).start()
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

millis = lambda : int (round (time.time() * 1000))

previousTime = 0
deltaTime = 0

counter = 1
time_acc = 0

# init plot
fig, ax = plt.subplots()
ax.set_title('Histogram (hue)')
ax.set_xlabel('Bin')
ax.set_ylabel('Frequency')

lw = 3
alpha = 0.5
bins = 256

lineGray, = ax.plot(np.arange(bins), np.zeros((bins,1)), c='k', lw=lw)
ax.set_xlim(0, bins-1)
ax.set_ylim(0, 1)
plt.ion()
plt.show()

while (not want_to_exit and cv2.getWindowProperty(win_name, 0) >= 0 ):

    ## Gestion de temps
    currentTime = millis()
    deltaTime = currentTime - previousTime
    previousTime = currentTime
    
    time_acc += deltaTime

    ## Gestion de la lecture
    retval, frame = cap.read()


    ## Pipeline
    
    # ROI
    roi = frame[:, left_roi:right_roi]
    roi_2 = frame[top_roi:bottom_roi, left_roi:right_roi]

    img_hue, img_sat, img_val = cv2.split (cv2.cvtColor(roi_2, cv2.COLOR_BGR2HSV))

    hist = cv2.calcHist([img_hue], [0], None, [bins], [0, bins]) / num_pixels

    lineGray.set_ydata(hist)

    cv2.rectangle(frame, (left_roi, top_roi), (left_roi + (right_roi - left_roi), top_roi + (bottom_roi - top_roi)), (0, 255, 0), 2)
    
    ## Affichage et autres sorties
    if (counter >= 30 ):
        counter = 0
        avg  =  time_acc / 30.0
        time_acc = 0

        print ( " Average per cycle : " + str (avg))

    counter += 1
    
    cv2.imshow(win_name, frame)
    #cv2.imshow(win_roi, roi)
    #cv2.imshow(win_roi_2, roi_2)
    cv2.imshow(win_hue, img_hue)

    fig.canvas.draw()
    
    ## Gestion des entrées
    key_val = cv2.waitKey(1) & 0xFF
    if key_val == 27:
        want_to_exit = True

    
cv2.destroyAllWindows()
cap.release()
