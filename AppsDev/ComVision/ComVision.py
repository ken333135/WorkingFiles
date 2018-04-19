# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 09:29:42 2018

@author: jingwenken
"""

import cv2
import glob, os

#filepath, RGB (1=as it is, 0=BW, -1=Colour)
img=cv2.imread("galaxy.jpg",0)

print(img)

#to show the img on screen
resized_image=cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))
cv2.imshow("Galaxy",resized_image)
#0 is to wait for button press, 2000 is to wait for 2sec to close window
cv2.waitKey(0)
cv2.imwrite("GalaxyResized.jpg",resized_image)
cv2.destroyAllWindows()

os.chdir("./sample-images")
for file in glob.glob("*"):
    img=cv2.imread(file,-1)
    resized_img=cv2.resize(img,(100,100))
    cv2.imshow(file,resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("Resized_"+file,resized_img)
