# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 03:02:17 2019

@author: Christopher
"""
# 反轉訊號_利空
from kline_plot import candlePlot
import pandas as pd


taiex2015=pd.read_csv('taiex2015.csv',sep ='\t')

taiex2015.index=pd.to_datetime(taiex2015.Date,
    format='%Y-%m-%d')


Close13=taiex2015.Close
Open13=taiex2015.Open


Cloud=pd.Series(0,index=Close13.index)
for i in range(1,len(Close13)):
    if all([Close13[i]<Open13[i],\
            Close13[i-1]>Open13[i-1],\
            Open13[i]>Close13[i-1],\
            Close13[i]<0.5*(Close13[i-1]+Open13[i-1]),\
            Close13[i]>Open13[i-1]]):
        Cloud[i]=1


Trend=pd.Series(0,index=Close13.index)
for i in range(2,len(Close13)):
    if Close13[i-1]>Close13[i-2]>Close13[i-3]:
        Trend[i]=1

darkCloud=Cloud+Trend
darkCloud[darkCloud==2]


taiex201509=taiex2015['2015-09']
candlePlot(taiex201509,\
                  title='加權股價指數2015年09月份的日K線圖')

taiex201510=taiex2015['2015-10']           
candlePlot(taiex201510 ,\
                  title='加權股價指數2015年10月份的日K線圖')





