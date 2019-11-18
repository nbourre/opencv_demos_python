import cv2
import numpy as np

img = cv2.imread(r"c:\temp\dashcam.jpg")

px = img[100, 100]
b = px [0]
print ("Bleu :" + str(b))

#Numpy plus rapide
g = img.item(100, 100, 1)
print ("Vert : " + str(g))

r = img.item(100, 100, 2)
print ("Rouge : " + str(r))

#Propriété de l'image
print ("Forme : " + str(img.shape))
print ("Nb pixels : " + str(img.size))
print ("Type de pixels : " + str(img.dtype))

cv2.imshow("Original", img)

#Split de couche
coucheB, coucheG, coucheR = cv2.split(img)

cv2.imshow("Bleu", coucheB)
cv2.imshow("Vert", coucheG)
cv2.imshow("Rouge", coucheR)

#Région d'intérêt
roi =  img[:, 0:int(img.shape[1] / 2)]
roi = cv2.medianBlur(roi, 5)
img[:, 0:int(img.shape[1] / 2)] = roi

cv2.imshow("ROI", img)

#Fusion
coucheR.fill(0)

dst = cv2.merge((coucheB, coucheG, coucheR))
cv2.imshow("no red", dst)

cv2.waitKey(0)

cv2.destroyAllWindows()