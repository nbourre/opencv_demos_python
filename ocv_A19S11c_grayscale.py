import cv2
import numpy as np

# Pour les options
# cv2.IMREAD_GRAYSCALE
# cv2.IMREAD_GRAYSCALE
# cv2.IMREAD_GRAYSCALE
img = cv2.imread(r"c:\temp\dashcam.jpg", cv2.IMREAD_GRAYSCALE)

cv2.imshow('Grayscale', img)

cv2.waitKey(0)

cv2.destroyAllWindows()