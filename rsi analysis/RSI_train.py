# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 13:47:34 2019

@author: Christopher
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

id_2317=pd.read_csv('2317.csv',sep='\t')
id_2317.index=pd.to_datetime(id_2317.Date)
print(id_2317.head())

close=id_2317.Close
close_change=close-close.shift(1)##收盤價變化
close_change=close_change.dropna()
print('\n',close_change.head())

indexprc=close_change.index
up_prc=pd.Series(0,index=indexprc)
up_prc[close_change>0]=close_change[close_change>0]
down_prc=pd.Series(0,index=indexprc)
down_prc[close_change<0]=-close_change[close_change<0]
rsidata=pd.concat([close,close_change,up_prc,down_prc],axis=1)
rsidata.columns=['Close','closeChange','upPrc','downPrc']
rsidata=rsidata.dropna()
print('\n',rsidata.head())

smup=[]##平均上漲力度
smdown=[]##下跌力度
for i in range(6,len(up_prc)+1):   
    smup.append(np.mean(up_prc.values[(i-6):i],dtype=np.float32))
    smdown.append(np.mean(down_prc.values[(i-6):i],dtype=np.float32))

#計算rsi
rsi6=[100*smup[i]/(smup[i]+smdown[i]) for i in range(len(smup))]
indexRsi=indexprc[5:]
Rsi6=pd.Series(rsi6,index=indexRsi)
rsi=Rsi6.head()
print('\n',rsi,'\n')

rsi_describe=Rsi6.describe()
print(rsi_describe)


##函數形式
def rsi(price,period=6):
    closeDif=(price-price.shift(1)).dropna()
    upPrc=pd.Series(0,index=closeDif.index)
    upPrc[closeDif>0]=closeDif[closeDif>0]
    downPrc=pd.Series(0,index=closeDif.index)
    downPrc[closeDif<0]=-closeDif[closeDif<0]
    rsi=[]
    for i in range(period,len(upPrc)+1):
        up_mean = np.mean(upPrc.values[(i-period):i],\
        dtype=np.float32)
        up_down = np.mean(downPrc.values[(i-period):i],\
        dtype=np.float32)
        rsi.append(100*up_mean/(up_mean+up_down))
    rsi=pd.Series(rsi,index=closeDif.index[(period-1):])
    return(rsi)
    
##計算股價12日RSI值
rsi12=rsi(close,12)
rsi12.tail()

##計算股價24日RSI值
rsi24=rsi(close,24)
rsi24.tail()

plt.plot(rsi24)
plt.title('RSI24的超買線和超賣線')
plt.ylim(-10,110)
plt.axhline(y=80,color='red')
plt.axhline(y=20,color='red')
plt.show()


#收盤價和6日RSI的曲線圖
plt.subplot(211)
plt.plot(close[Rsi6.index])
plt.ylabel('Close')
plt.title('鴻海股票收盤價')

plt.subplot(212)
plt.plot(Rsi6)
plt.ylabel('Rsi6')
plt.title('鴻海股票6日RSI')
plt.show()

#黃金交叉和死亡交叉
plt.plot(Rsi6,label='Rsi6')
plt.plot(rsi24,
         label='Rsi24',color='red',\
         linestyle='dashed')
plt.title('RSI黃金交叉和死亡交叉')
plt.ylim(-10,110)
plt.legend()
plt.show()
