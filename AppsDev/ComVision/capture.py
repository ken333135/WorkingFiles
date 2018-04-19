# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 10:06:34 2018

@author: jingwenken
"""

import cv2, time
from datetime import datetime
import pandas

first_frame=None
status_list=[None,None]
times=[]
video=cv2.VideoCapture(0)

while True:
    check, frame=video.read()
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)
    #in the first iteration, use the first frame as the base frame for future comparisons
    if first_frame is None:
        first_frame=gray
        #skips all code below and goes back to the top of the loop
        continue
    delta_frame=cv2.absdiff(first_frame,gray)
    #parameter(frame,threshold value,color to assign to those above Threshold,cv2.THRESH_BINARY)
    threshold_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    threshold_frame=cv2.dilate(threshold_frame,None,iterations=2)
    #to detect and show contours
    (_,cnts,_)=cv2.findContours(threshold_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in cnts:
        #if area of contour is less than 1000 pixels, then continue to next contour
        if cv2.contourArea(contour) < 10000:
            continue
        #this is where python detech a big object moving in the frame, so we change the status from 0 to 1
        status=1
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        
    status_list.append(status)
    
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())
    
    cv2.imshow("Gray",gray)
    cv2.imshow("Capturing",delta_frame)
    cv2.imshow("Threshold Frame",threshold_frame)
    cv2.imshow("Color Frame",frame)
    print(status)
    key=cv2.waitKey(1)
    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break

video.release()
cv2.destroyAllWindows()

print(times)
df=pandas.DataFrame(columns=["Start","End"])
for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
df.to_csv("Capture.csv")
    
print(df)