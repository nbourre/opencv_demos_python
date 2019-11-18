from threading import Thread

import cv2
import numpy as np
import os
import pyaudio


#List des constantes d'application
CANNY_THRESHOLD_MAX = 250
CANNY_THRESHOLD_MIN = 80
DIM_SOBEL = 3
MIN_OBJECT_PERIMETER = 1250
KILL_BRIGADIER_AREA = 140000
TONE_AREA_THRESHOLD = 80000

#Objet de capture des frames
capture = cv2.VideoCapture(0)

#Dictionnaire servant à entreposer la liste des contours d'un seul frame
contours = {}

#Tableau de contours de polygones
approx = []

#Objet de gestion de l'audio
p = pyaudio.PyAudio()


# Fonction qui ément un signal sonore lorsque la voiture est trop près du brigadier
def tone(frequency):

    volume = 1.0
    sampling_rate = 44100
    duration = 0.2

    samples = (np.sin(2 * np.pi * np.arange(sampling_rate * duration) * frequency / sampling_rate)).astype(np.float32)

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sampling_rate,
                    output=True)

    stream.write(volume * samples)

    stream.stop_stream()
    stream.close()


while(capture.isOpened()):

    # Capture d'une image dans la variable frame.  Si cela fonctionne, retourne True dans la variable result
    result, rgb_frame = capture.read()

    if result:

        # Retourne le résultat du filtre de Canny selon les valeurs de seuillage
        canny = cv2.Canny(rgb_frame, CANNY_THRESHOLD_MIN, CANNY_THRESHOLD_MAX, DIM_SOBEL)


        # Cette fonction retoune un tableau de contours d'une image binaire selon l'algorithme Suzuki85 suite au filtre de Canny
        # Pour plus d'information sur l'algorithme de Suzuki --> Suzuki, S. and Abe, K., Topological Structural Analysis
        # of Digitized Binary Images by Border Following. CVGIP 30 1, pp 32-46 (1985)
        im2, contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(0, len(contours)):


            # Cette fonction effectue un calcul approximatif de la différence d'une courbe ou d'un polygone avec une courbe
            # ou un polygone de référence possèdant moins d'arêtes dont la distance entre ces derniers est plus petite
            # ou égale à la précision spécifiée en "cv2.arcLength(contours[i], True) * 0.01" (le périmêtre)
            # Pour plus d'information voir l'algorithme de Douglas-Peucker
            # <http://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm>
            approx = cv2.approxPolyDP(contours[i], cv2.arcLength(contours[i], True) * 0.01, True)


            # Si la forme trouvé est plus petite que le minimum désiré, on ignore ce frame
            area = abs(cv2.contourArea(contours[i]))
            if area < MIN_OBJECT_PERIMETER:
                continue

            # Si la forme n'est pas convexe, on ignore ce frame
            if not(cv2.isContourConvex(approx)):
                continue

            # Nombre d'arêtes dans une forme polygonale (donc convexe)
            verticle = len(approx)

            if verticle == 8:

                if area < KILL_BRIGADIER_AREA:
                    cv2.drawContours(rgb_frame, [approx], -1, (255, 0, 0), -1)

                # Si on est rendu vraiment proche du brigadier, on émet un signal sonore.
                if area > TONE_AREA_THRESHOLD and area < KILL_BRIGADIER_AREA:
                    thread = Thread(target=tone, args=(440, ))
                    thread.start()

                if area > KILL_BRIGADIER_AREA:
                    os.system('say "Oh my god, you killed the brigadier"')

        # Affichage du résultat à l'écran
        #cv2.imshow('Avec le filtre de canny', canny)
        cv2.imshow('Ne tuez pas le brigadier', rgb_frame)

        # Laisse le temps à l'affichage de respirer un peu
        cv2.waitKey(1)

capture.release()
cv2.destroyAllWindows()