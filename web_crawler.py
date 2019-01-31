# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 23:29:21 2019

@author: User
"""

import requests
import json
import csv
import time, datetime,os
from bs4 import BeautifulSoup

dt = datetime.datetime.now()
dt.year
stock_list = ['2834'] #inout the stock IDs ¥x¥ø»È
now = datetime.datetime.now()
year_list = range (2011,now.year+1) #since 2011 to this year
month_list = range(1,13)  # 12 months

#standard web crawing process
def get_infos (year, month, stock_id):
    date = str (year) + "{0:0=2d}".format(month) +'01' ## format is yyyymmdd
    sid = str(stock_id)
    url_twse = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+date+'&stockNo='+sid
    res =requests.post(url_twse,)
    soup = BeautifulSoup(res.text , 'html.parser')
    smt = json.loads(soup.text)     #convert data into json
    return smt

def write_csv(stock_id,directory,filename,smt) :
    writefile = directory + filename               #set output file name
    outputFile = open(writefile,'w',newline='')
    outputWriter = csv.writer(outputFile)
    head = ''.join(smt['title'].split())
    a = [head,""]
    outputWriter.writerow(a)
    outputWriter.writerow(smt['fields'])
    for data in (smt['data']):
        outputWriter.writerow(data)

    outputFile.close()
    
    
#create a directory in the current one doesn't exist
def makedirs (year, month, stock_id):
    sid = str(stock_id)
    yy  = str(year)
    directory = 'D:/stock'+'/'+sid +'/'+ yy
    if not os.path.isdir(directory):
        os.makedirs (directory)  # os.makedirs able to create multi folders
        
for stock_id in stock_list:
    for year in year_list:
        for month in month_list:
            if (dt.year == year and month > dt.month) :break  # break loop while month over current month
            sid = str(stock_id)
            yy  = str(year)
            mm  = month
            directory = 'D:/stock'+'/'+sid +'/'+yy +'/'       #setting directory
            filename = str(yy)+str("%02d"%mm)+'.csv'          #setting file name
            smt = get_infos(year ,month, stock_id)           #put the data into smt 
            makedirs (year, month, stock_id)                  #create directory function
            write_csv (stock_id,directory, filename, smt)    # write files into CSV
            time.sleep(5)
###http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20181212&stockNo=1001
            

        
