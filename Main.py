__author__ = 'CFWei'
from GetFeature import *
from GetStock import *
import csv
from datetime import datetime,timedelta

isGetStock = 0
isGetDJI = 0
isGetsp500energy = 0
startDate = ('2014/12/28')
dataPerStockCount = 200
#Get Stock
if isGetStock == 1:
    f=open('AllStockList','r')
    for line in f:
        stockNum = line.strip()
        getStock(startDate,int(stockNum))
        print(line.strip())

if isGetDJI == 1:
    getDJI(startDate)

if isGetsp500energy == 1:
    getsp500energy(startDate)


f=open('ParseStockList','r')
with open('names.csv', 'w', newline='') as csvfile:
    #定義Field Title
    fieldnames = ['date','OpenPrice','HighPrice','LowPrice','ClosePrice','Volume','DJI','MACD','BankInterest','WorkingPeoplePercentage','SP500Energy']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #將Title
    writer.writeheader()
    #讀取要抓取的股票號碼
    for line in f:
        stockNum = line.strip()
        dSearchDate = datetime.strptime(startDate,"%Y/%m/%d")
        dataCount = 0
        #開始抓取設定的時間區間的股票資訊
        while(1):
            #判斷是不是六日，若是六日則跳過
            weekDay = dSearchDate.strftime("%w")
            searchDate = dSearchDate.strftime("%Y/%m/%d")
            dSearchDate = dSearchDate - timedelta(days=1)
            if weekDay == "6" or weekDay=="0":
                continue
            else:
                tmp = {}
                tmp["date"] = searchDate
                tmp["OpenPrice"] = OpenPrice(searchDate,int(stockNum))
                tmp["HighPrice"] = HighPrice(searchDate,int(stockNum))
                tmp["LowPrice"] = LowPrice(searchDate,int(stockNum))
                tmp["ClosePrice"] = ClosePrice(searchDate,int(stockNum))
                tmp["Volume"] = Volume(searchDate,int(stockNum))
                tmp["DJI"] = DJI(searchDate,int(stockNum))
                tmp["MACD"] = MACD(searchDate,int(stockNum))
                tmp["BankInterest"] = BankInterest(searchDate,int(stockNum))
                tmp["WorkingPeoplePercentage"] = WorkingPeoplePercentage(searchDate,int(stockNum))
                tmp["SP500Energy"] = SP500Energy(searchDate,int(stockNum))
                writer.writerow(tmp)

                dataCount = dataCount + 1
                if dataCount == dataPerStockCount:
                    break




