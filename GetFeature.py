__author__ = 'CFWei'
import talib

import csv
from numpy import *
from GetStock import *
import datetime
filePath="stock/"

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

def DJI(date,stockNum):
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
        print("MACD Error:"+date+" "+str(stocknum))
        return 0

def BankInterest(date,stockNum):
    try:
        searchDateTime = datetime.datetime.strptime(date,"%Y/%m/%d")
        #轉成民國
        year = str((int(searchDateTime.strftime('%Y'))-1911))
        month = searchDateTime.strftime('%m')
        tmpDate = year + "/" + month
        with open(filePath+"bank_interest.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == tmpDate:
                    return row[1]
        return 0
    except:
        print("BankInterest Error:"+date+" "+str(stockNum))
        return 0

def WorkingPeoplePercentage(date,stockNum):
    try:
        searchDateTime = datetime.datetime.strptime(date,"%Y/%m/%d")
        #轉成民國
        year = str((int(searchDateTime.strftime('%Y'))-1911))
        month = searchDateTime.strftime('%m')
        tmpDate = year + "/" + month
        with open(filePath+"WorkingPeoplePercentage.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == tmpDate:
                    return row[1]
        return 0
    except:
        print("WorkingPeoplePercentage Error:"+date+" "+str(stockNum))
        return 0

def SP500Energy(date,stockNum):
    try:
        return parseStock(date,"SPList",4)
    except:
        print("SP500Energy Error:"+date+" "+str(stockNum))
        return 0

def getStockInfo(date, stockNum,dataLength):

    DataCount = dataLength
    searchDateTime = datetime.datetime.strptime(date, "%Y/%m/%d")
    #Record How many days are used
    dateCount=0
    #Record How many data are used
    count = 0

    closePrice = []
    openPrice = []
    highPrice = []
    lowPrice = []
    volume = []

    while(1):
        tmpDate = searchDateTime - datetime.timedelta(days=dateCount)
        tmpClosePrice = ClosePrice(tmpDate.strftime("%Y/%m/%d"), stockNum)
        tmpOpenPrice = OpenPrice(tmpDate.strftime("%Y/%m/%d"), stockNum)
        tmpHighPrice = HighPrice(tmpDate.strftime("%Y/%m/%d"), stockNum)
        tmpLowPrice = LowPrice(tmpDate.strftime("%Y/%m/%d"), stockNum)
        tmpVolume = Volume(tmpDate.strftime("%Y/%m/%d"), stockNum)

        if tmpClosePrice != 0:
            count = count + 1
            closePrice.append(float(tmpClosePrice))
            openPrice.append(float(tmpOpenPrice))
            highPrice.append(float(tmpHighPrice))
            lowPrice.append(float(tmpLowPrice))
            volume.append(float(tmpVolume))

        dateCount = dateCount +1
        if count >= DataCount:
            break

    closePrice.reverse()
    openPrice.reverse()
    highPrice.reverse()
    lowPrice.reverse()
    volume.reverse()

    outResult = {
        'open': array(openPrice),
        'high': array(highPrice),
        'low': array(lowPrice),
        'close': array(closePrice),
        'volume': array(volume)
    }

    return outResult

def RelativeStrengIndex(date, stockNum):
    try:
        optTimeperiod = 14
        stockInfo = getStockInfo(date, stockNum, optTimeperiod+1)

        outRSI = talib.RSI(stockInfo['close'], optTimeperiod)

        return outRSI[len(outRSI)-1]
    except:
        return 0

def StochasticIndex(date,stockNum):
    try:

        optInFastkPeriod = 5
        optInSlowkPeriod = 3
        optInSlowkMatype = 0
        optInSlowdPeriod = 3
        optInSlowdMatype = 0
        optTimeperiod = 9

        stockInfo = getStockInfo(date, stockNum, optTimeperiod)
        outSlowk, outSlowd = talib.STOCH(stockInfo['high'], stockInfo['low'], stockInfo['close'], optInFastkPeriod, optInSlowkPeriod, optInSlowkMatype, optInSlowdPeriod, optInSlowdMatype)


        return outSlowk[len(outSlowk)-1]
    except:
        return 0

def OnBalanceVolume(date, stockNum):
    try:
        optTimeperiod = 30
        stockInfo = getStockInfo(date, stockNum, optTimeperiod+1)

        outOBV = talib.OBV(stockInfo['close'], stockInfo['volume'])

        return outOBV[len(outOBV)-1]
    except:
        return 0

def MovingAverage(date, stockNum):
    try:
        optTimeperiod = 30
        optMatype = 0

        stockInfo = getStockInfo(date, stockNum, optTimeperiod)

        outMA = talib.MA(stockInfo['close'], optTimeperiod,optMatype)

        return outMA[len(outMA)-1]
    except:
        return 0

def UppaerBollingerBands(date, stockNum):
    outType = 1
    return BollingerBands(date, stockNum, outType)

def MiddleBollingerBands(date, stockNum):
    outType = 2
    return BollingerBands(date, stockNum, outType)

def LowerBollingerBands(date, stockNum):
    outType = 3
    return BollingerBands(date, stockNum, outType)

def BollingerBands(date, stockNum, outType):
    try:
        optTimeperiod = 5
        optNbdevup = 2
        optNbdevdn = 2
        optMatype = 0

        stockInfo = getStockInfo(date, stockNum, optTimeperiod)

        upperBand, middleBand, lowerBand = talib.BBANDS(stockInfo['close'], optTimeperiod, optNbdevup, optNbdevdn, optMatype)

        if outType == 1:
            outResult = upperBand
        elif outType == 2:
            outResult = middleBand
        elif outType == 3:
            outResult = lowerBand
        else:
            outResult = middleBand

        return outResult[len(outResult)-1]
    except:
        return 0

def Momentum(date, stockNum):
    try:
        optTimeperiod = 10

        stockInfo = getStockInfo(date, stockNum, optTimeperiod+1)

        outMOM = talib.MOM(stockInfo['close'], optTimeperiod)

        return outMOM[len(outMOM)-1]
    except:
        return 0

def WilliamsR(date, stockNum):
    try:
        optTimeperiod = 14
        stockInfo = getStockInfo(date, stockNum, optTimeperiod)
        outWILLR = talib.WILLR(stockInfo['high'], stockInfo['low'], stockInfo['close'], optTimeperiod)

        return outWILLR[len(outWILLR)-1]
    except:
        return 0

#print(BankInterest('2014/08/28','3704'))

#outMACD ,outMACDSignal ,outMACDHist=talib.MACD(close,12,26,9)
#print(outMACD)
