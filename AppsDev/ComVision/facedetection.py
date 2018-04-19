# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 09:55:01 2018

@author: jingwenken
"""

import cv2
import os

os.chdir("./Files")
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

img=cv2.imread("news.jpg")
gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

faces=face_cascade.detectMultiScale(gray_img,
                                    scaleFactor=1.05,
                                    minNeighbors=5)
print(faces)
#values in faces are (column of topleftfacebox,row of topleftfacebox,width,height of box)

for x,y,w,h in faces:
    #parameter are (topleftcoord,bottomrightcoord,color in RGB,thickness of rectangle)
    img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)

cv2.imshow("Gray",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

