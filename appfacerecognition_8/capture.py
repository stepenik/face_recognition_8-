##########################################################################################
#                   UNIVERSIDAD TECNICA PARTICULAR DE LOJA                               #
#....................................................................................... #
#DEVELOPMENT OF AN APPLICATION FOR FACIAL RECOGNITION USING THE ALGORITHM FISHERFACES    #
#                                                                                        #
#Authors: Carlos Saca (cfsaca@utpl.edu.ec), Critian Ortiz (ceortiz2@utpl.edu.ec)         #
#Professor: Ing. Luis Rodrigo Barba                                                      #
#Date: 16/01/2017                                                                        #
#........................................................................................#
#System Requirements:                                                                    #
#Ubuntu: 16.4                                                                            #
#Python: 2.7+                                                                            #
#OpenCv: 3.0.0                                                                           #
##########################################################################################
import os
import numpy as np
import cv2, sys 
size = 4
fn_haar = 'haarcascade_frontalface_alt.xml'
fn_dir = 'rostros'
fn_name = sys.argv[1]
path = os.path.join(fn_dir, fn_name)
if not os.path.isdir(path):
    os.mkdir(path)
(im_width, im_height) = (112, 92)
haar_cascade = cv2.CascadeClassifier(fn_haar)
webcam = cv2.VideoCapture(0)

#Capture faces
count = 0
while count < 100:#Controls the number of catches
    (rval, im) = webcam.read()
    im = cv2.flip(im, 1, 0)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    mini = cv2.resize(gray, (gray.shape[1] / size, gray.shape[0] / size))
    faces = haar_cascade.detectMultiScale(mini)
    faces = sorted(faces, key=lambda x: x[3])
    if faces:
        face_i = faces[0]
        (x, y, w, h) = [v * size for v in face_i]
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))
        pin=sorted([int(n[:n.find('.')]) for n in os.listdir(path)
               if n[0]!='.' ]+[0])[-1] + 1
	#We save the images
        cv2.imwrite('%s/%s.png' % (path, pin), face_resize)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(im, fn_name, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,
            1,(0, 255, 0))
        count += 1
    cv2.imshow('OpenCV', im)
    key = cv2.waitKey(10)
    if key == 27:
        break