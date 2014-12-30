__author__ = 'CFWei'
from GetFeature import *
from GetStock import *
import csv

isGetStock=0
isGetDJI=0
isGetsp500energy=0

startDate=('2014/12/28')
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
    fieldnames = ['y','OpenPrice','HighPrice','LowPrice','ClosePrice','Volume','DJI','MACD','BankInterest','WorkingPeoplePercentage','SP500Energy']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for line in f:
        stockNum = line.strip()
        searchDate = '2014/08/25'
        tmp = {}
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




