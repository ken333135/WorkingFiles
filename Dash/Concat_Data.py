# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 16:17:08 2018

@author: jingwenken
"""
import os
import pandas as pd
import glob

os.chdir(r'C:\Users\jingwenken\Desktop\Ken\CTMO\SnC_RDB_Data\20180529\BSD-DIAG\Hist_Data\Accelerometer')

try:
    os.remove('MedianAccelerationsHist.csv')
except:
    None

files = glob.glob(r'C:\Users\jingwenken\Desktop\Ken\CTMO\SnC_RDB_Data\20180529\BSD-DIAG\Hist_Data\Accelerometer\\'+'*.csv')
if '*MedianAccelerationHist.csv' in files:
    print('yesss')
    os.remove('MedianAccelerationsHist.csv')
    files = glob.glob(r'C:\Users\jingwenken\Desktop\Ken\CTMO\SnC_RDB_Data\20180529\BSD-DIAG\Hist_Data\Accelerometer\\'+'*.csv')

columns = ['VOBC',' Acc0',' Acc1',' Date']
data = pd.DataFrame(columns=columns)

for file in files:
    temp = pd.read_csv(file)
    data = pd.concat([data,temp])

data.to_csv('MedianAccelerationsHist.csv',index=False)
print(data.shape)