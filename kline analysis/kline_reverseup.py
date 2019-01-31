# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 02:37:22 2019

@author: Christopher
"""
from kline_plot import candlePlot
import pandas as pd

#反轉訊號_利多
taiex2015=pd.read_csv('taiex2015.csv',sep='\t')
taiex2015.index=pd.to_datetime(taiex2015.Date,
    format='%Y-%m-%d')

head=taiex2015.head(2)
print(head)
tail=taiex2015.iloc[-2:,:]
print(tail)

Close=taiex2015.Close   #收盤價
Open=taiex2015.Open     #開盤價
ClOp=Close-Open    #價差
price=ClOp.head()
print(price)

describe=ClOp.describe()    #價差分布狀況
print('\n',describe)


Shape = [0,0,0] #K棒類型
for i in range(3,len(ClOp)):
    if all([ClOp[i-2]<-20,abs(ClOp[i-1])< 20,\
    ClOp[i]>5,abs(ClOp[i])>abs(ClOp[i-2]*0.5)]):
        Shape.append(1)
    else:
        Shape.append(0)

print(Shape.index(1))

#捕捉十字反轉訊號K線圖
Doji=[0,0,0]
for i in range(3,len(Open)):
    if all([Open[i-1]<Open[i],Open[i-1]<Close[i-2],\
    Close[i-1]<Open[i],(Close[i-1]<Close[i-2])]):
        Doji.append(1)
    else:
        Doji.append(0)

Doji.count(1)

#向下趨勢
Trend=[0,0,0]
for i in range(3,len(Close)):
    if Close[i-2] < Close[i-3]:
        Trend.append(1)
    else:
        Trend.append(0)
        
StarSig=[]
for i in range(len(Trend)):
    if all([Shape[i]==1,Doji[i]==1,Trend[i]==1]):
        StarSig.append(1)
    else:
        StarSig.append(0)

for i in range(len(StarSig)):
    if StarSig[i]==1:
        print(taiex2015.index[i])

taiex201508=taiex2015['2015-08']

candlePlot(taiex201508, title=' 加權股價指數2015年8月份的日K線圖')