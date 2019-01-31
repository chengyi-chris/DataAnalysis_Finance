# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 14:39:59 2019

@author:  Christopher
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

weichuan=pd.read_csv('1201.csv',sep='\t')
weichuan.index=pd.to_datetime(weichuan.Date)
close=weichuan.Close
rsi6=rsi(close,6)
rsi24=rsi(close,24)

#rsi6捕捉買賣點
Sig1=[]
for i in rsi6:
    if i>80:
        Sig1.append(-1)
    elif i<20:
        Sig1.append(1)
    else:
        Sig1.append(0)

date1=rsi6.index
Signal1=pd.Series(Sig1,index=date1)
sign_pos=Signal1[Signal1==1].head(n=3)
print('\n',sign_pos)

sign_neg=Signal1[Signal1==-1].head(n=3)
print('\n',sign_neg)


#交易訊號:黃金交叉與死亡交叉
Signal2=pd.Series(0,index=rsi24.index)
lagrsi6= rsi6.shift(1)
lagrsi24= rsi24.shift(1)
for i in rsi24.index:
    if (rsi6[i]>rsi24[i]) & (lagrsi6[i]<lagrsi24[i]):
        Signal2[i]=1
    elif (rsi6[i]<rsi24[i]) & (lagrsi6[i]>lagrsi24[i]):
        Signal2[i]=-1
        
#合併交易訊號
signal=Signal1+Signal2
signal[signal==2] = 1
signal[signal==-2] = -1
signal=signal.dropna()


trad_sig=signal.shift(1)
#股票收益率        
ret=close/close.shift(1)-1
retprint=ret.head()
print('\n',retprint)        

#作多收益率        
ret=ret[trad_sig.index]
buy=trad_sig[trad_sig==1]
buyRet=ret[trad_sig==1]*buy
#作空收益率
sell=trad_sig[trad_sig==-1]
sellRet=ret[trad_sig==-1]*sell
#買賣交易合併收益率
trade_ret=ret*trad_sig


plt.subplot(211)
plt.plot(buyRet,label='buyRet',color='g')
plt.plot(sellRet,label='sellRet',
    color='r',linestyle='dashed')
plt.title('味全股票RSI指標交易策略')
plt.ylabel('strategy return')
plt.legend()
plt.subplot(212)
plt.plot(ret,'b')
plt.ylabel('stock return')
plt.show()        
        
##預測正確與失敗的收益率
def strat(tradeSignal,ret):
    ret=ret[tradeSignal.index]
    tradeRet=ret*tradeSignal
    tradeRet[tradeRet==(-0)]=0
    winRate=len(tradeRet[tradeRet>0])/len(\
           tradeRet[tradeRet!=0])
    meanWin=sum(tradeRet[tradeRet>0])/len(\
            tradeRet[tradeRet>0])
    meanLoss=sum(tradeRet[tradeRet<0])/len(\
             tradeRet[tradeRet<0])
    perform={'winRate':winRate,\
    'meanWin':meanWin,\
    'meanLoss': meanLoss}
    return(perform)

only_buy=strat(buy,ret)
only_sell=strat(sell,ret)
Trade=strat(trad_sig,ret)
Test=pd.DataFrame({"BuyOnly":only_buy,\
        "SellOnly":only_sell,"Trade":Trade})
print('\n',Test)

##累積報酬率圖
cumStock=np.cumprod(1+ret)-1
cumTrade=np.cumprod(1+trade_ret)-1

plt.subplot(211)
plt.plot(cumStock)
plt.ylabel('cumulative return of stock')
plt.title('原始累積收益率')
plt.subplot(212)
plt.plot(cumTrade)
plt.ylabel('cumulative return of strategy')
plt.title('RSI指標交易策略累積收益率')