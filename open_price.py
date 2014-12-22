__author__ = 'CFWei'
import talib
import time
import datetime
from numpy import *

from GetStock import getStock,parseStock,getDJI

def OpenPrice(date,stockNum):
    return parseStock(date,stockNum,1)

def HighPrice(date,stockNum):
    return parseStock(date,stockNum,2)

def LowPrice(date,stockNum):
    return parseStock(date,stockNum,3)

def ClosePrice(date,stockNum):
    return parseStock(date,stockNum,4)

def Volume(date,stockNum):
    return parseStock(date,stockNum,5)

def DJI(date):
    return parseStock(date,"DJI",4)

def MACD(date,stocknum):
    try:
        optInFastPeriod = 28
        optInSlowPeriod = 12
        optInSignalPeriod = 9
        DataCount= optInFastPeriod + optInSignalPeriod - 1
        searchDateTime = datetime.datetime.strptime(date,"%Y/%m/%d")
        #Record How many days are used
        dateCount=0
        #Record How many data are ured
        count = 0
        closePrice = []
        while(1):
            tmpDate = searchDateTime - datetime.timedelta(days=dateCount)
            tmpClosePrice = ClosePrice(tmpDate.strftime("%Y/%m/%d"),stocknum)
            if tmpClosePrice != 0:
                count = count + 1
                closePrice.append(float(tmpClosePrice))
            dateCount = dateCount +1
            if count >= DataCount:
                break
        closePrice.reverse()
        outMACD ,outMACDSignal ,outMACDHist=talib.MACD(array(closePrice),optInFastPeriod,optInSlowPeriod,optInSignalPeriod)
        return outMACD[len(outMACD)-1]
    except:
        return 0

def BankInteerst(date,stocknum):
    searchDateTime = datetime.datetime.strptime(date,"%Y/%m/%d")

MACD('2014/12/01',3705)

#outMACD ,outMACDSignal ,outMACDHist=talib.MACD(close,12,26,9)
#print(outMACD)
