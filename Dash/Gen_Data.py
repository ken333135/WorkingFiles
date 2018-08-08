# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 14:50:47 2018

@author: jingwenken
"""
import pandas as pd
import os
import numpy as np
from datetime import datetime
from datetime import timedelta

os.chdir(r'C:\Users\jingwenken\Desktop\Ken\CTMO\SnC_RDB_Data\20180529\BSD-DIAG\Hist_Data\Accelerometer')

data = pd.read_csv('MedianAccelerations_20180529.csv')
date = datetime.strptime(str(data[' Date'].iloc[1]),"%Y%m%d")

#time delta of 1 day
day = timedelta(days=1)

VOBC = list(data['VOBC'])
size = 10

for i in range(0,60):
    date = date + day
    acc0 = list(np.random.randint(size,size=len(VOBC))/1000)
    acc1 = list(np.random.randint(size,size=len(VOBC))/1000)
    dates = list([str(date.strftime("%Y%m%d"))]*len(VOBC))
    data_new = pd.DataFrame([VOBC,acc0,acc1,dates]).T
    data_new.columns = data.columns
    data_new.to_csv('MedianAccelerations_'+str(date.strftime("%Y%m%d"))+'.csv',index=False)
    i = i+1
    size = size+2
    

