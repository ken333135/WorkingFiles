# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 13:54:54 2018

@author: jingwenken
"""

import cv2
im_g=cv2.imread("smallgray.png",1)
print(im_g)

cv2.imwrite("newsmallgray.png",im_g)