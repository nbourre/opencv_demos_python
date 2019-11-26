import cv2
import sys
import numpy as np

img = cv2.imread(sys.argv[1])

win_main = 'Main'
win_erode = 'Erosion'
win_dilate = 'Dilatation'

key_val = 0

kernel = np.ones((5, 5), np.uint8)
dirty_data = True

img_erosion = img
img_dilatation = img

iterations = 1

while (key_val != 27):
    key_val = cv2.waitKey(1) & 0xFF

    if (key_val == ord('+') or key_val == ord('=')):
        dirty_data = True
        iterations = min(5, iterations + 1)
    if (key_val == ord('-')):
        dirty_data = True
        iterations = max(1, iterations - 1)


    if (dirty_data):
        dirty_data = False
        img_erosion = cv2.erode(img, kernel, iterations=iterations)
        img_dilatation = cv2.dilate(img, kernel, iterations=iterations)
    
    cv2.imshow(win_erode, img_erosion)
    cv2.imshow(win_main, img)
    cv2.imshow(win_dilate, img_dilatation)

cv2.destroyAllWindows()