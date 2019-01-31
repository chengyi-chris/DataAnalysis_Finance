# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 23:55:51 2019

@author: Christopher
"""
import pandas as pd 
from matplotlib.dates import date2num
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from mpl_finance import  candlestick_ohlc
from kline_plot import candlePlot
#讀取外部 CSV 資料
taiex2015=pd.read_csv('taiex2015.csv',sep='\t')
print(taiex2015.head(n=5))

taiex2015.index=pd.to_datetime(taiex2015.Date)
type(taiex2015.index)#轉成DatetimeIndex類型

taiex201508=taiex2015['2015-08']
print(taiex201508.head(n=5))

taiex201508.Date=[date2num(datetime.strptime(date,"%Y-%m-%d"))\
                  for date in taiex201508.Date]
##字串轉浮點數格式 並依照年月日 分割
print(taiex201508.head(n=5))
type(taiex201508)
##DataFrame轉為Sequence
"""
taiex201508_listData=[]
for i in range(len(taiex201508)):
    a=[taiex201508.Date[i],\
    taiex201508.Open[i],taiex201508.High[i],\
    taiex201508.Low[i],taiex201508.Close[i]]
    taiex201508_listData.append(a)
    

ax= plt.subplot()
mondays = WeekdayLocator(MONDAY)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(DayLocator() )
weekFormatter = DateFormatter('%y %b %d')
ax.xaxis.set_major_formatter(weekFormatter)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
ax.set_title('加權股價指數2015年8月份K線圖')
candlestick_ohlc(ax, taiex201508_listData, 
    width=0.7,colorup='r', colordown='g');
plt.setp(plt.gca().get_xticklabels(),
    rotation=50,
    horizontalalignment='center') """

candlePlot(taiex201508,title='加權股價指數2015年8月份K線圖')
plt.show()