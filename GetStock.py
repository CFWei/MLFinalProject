__author__ = 'CFWei'
from bs4 import BeautifulSoup
import urllib.request
import os
import csv

from datetime import datetime

filePath="stock/"

def getStock(date,stockNum):
    try:
        searchDateTime = datetime.strptime(date,"%Y/%m/%d")
        endTime_y = searchDateTime.strftime("%Y")
        endTime_m = str(int(searchDateTime.strftime("%m"))-1)
        endTime_d = searchDateTime.strftime("%d")

        startTime_y = str(2010)
        startTime_m = str(1-1)
        startTime_d = str(1)

        #Get Stock File
        url= "http://real-chart.finance.yahoo.com/table.csv?s="+str(stockNum)+".TW&d="+endTime_m+"&e="+endTime_d+"&f="+endTime_y+"&g=d&a="+startTime_m+"&b="+startTime_d+"&c="+startTime_y+"&ignore=.csv"
        response = urllib.request.urlopen(url)
        csv_result = response.read().decode('utf-8')

        #Save File
        if not os.path.exists(filePath):
            os.mkdir(filePath)
        file = open(filePath+str(stockNum), 'w', encoding='utf-8')
        file.write(csv_result)
        file.close()
    except:
        print(str(stockNum)+" Get Stock Error")

def getDJI(date):
    try:
        searchDateTime = datetime.strptime(date,"%Y/%m/%d")
        endTime_y = searchDateTime.strftime("%Y")
        endTime_m = searchDateTime.strftime("%b")
        endTime_d = searchDateTime.strftime("%d")

        startTime_y = str(2010)
        startTime_m = "Jan"
        startTime_d = str(1)

        url = "http://www.google.com/finance/historical?q=INDEXDJX%3A.DJI&ei=oWwmVKCtJYSTlAX03oGICg&&num=200&startdate=" + startTime_m + "+" + startTime_d + "+" + startTime_y + "&enddate=" + endTime_m + "+" + endTime_d + "+" + endTime_y

        #Get Response From URL
        response=urllib.request.urlopen(url)
        #Get Byte Array From URL Content
        html = response.read()
        #Convert Byte Array to String
        shtml = html.decode('utf-8')

        #Create BeautifulSoup
        soup = BeautifulSoup(shtml, 'lxml')

        priceTable = soup.find_all(id='prices')

        #Get DJI Title
        DJITitle=[]
        for title in priceTable[0].find_all('th' , class_ = 'bb'):
            DJITitle.append(title.contents[0].strip('\n'))

        #Get DJI List
        DJIList = []
        for child in priceTable[0].find_all('tr'):
            temp = []
            for child1 in child.find_all('td'):
                temp.append(child1.contents[0].strip(',').strip('\n').replace(',', ''))

            if temp != []:
                DJIList.append(temp)
        #Save to file
        file = open(filePath+'DJI', 'w', encoding='utf-8')
        flag = 0
        for title in DJITitle:
            if flag !=0:
                file.write(',')
            else:
                flag=flag+1
            file.write(title)
        file.write('\n')
        for items in DJIList:
            flag = 0
            for item in items:
                if flag == 0:
                    date = item.split(' ')
                    month = datetime.strptime(date[0],"%b").strftime('%m')
                    if len(date[1]) == 1:
                        date[1] = '0' + date[1]
                    day =  datetime.strptime(date[1],"%d").strftime('%d')
                    year = date[2]
                    file.write(year+'-'+month+'-'+day)
                    flag = 1
                else:
                    file.write(',')
                    file.write(item)

            file.write('\n')
        file.close()

    except:
        print('Get DJI Fail')

def getsp500energy(date):
    try:
        searchDateTime = datetime.strptime(date,"%Y/%m/%d")
        endTime_y = searchDateTime.strftime("%Y")
        endTime_m = searchDateTime.strftime("%b")
        endTime_d = searchDateTime.strftime("%d")

        startTime_y = str(2010)
        startTime_m = "Jan"
        startTime_d = str(1)

        url = "https://www.google.com/finance/historical?q=INDEXSP%3ASP500-10&num=200&startdate=" + startTime_m + "+" + startTime_d + "+" + startTime_y + "&enddate=" + endTime_m + "+" + endTime_d + "+" + endTime_y
        #Get Response From URL
        response=urllib.request.urlopen(url)
        #Get Byte Array From URL Content
        html = response.read()
        #Convert Byte Array to String
        shtml = html.decode('utf-8')

        #Create BeautifulSoup
        soup = BeautifulSoup(shtml, 'lxml')
        priceTable = soup.find_all(id='prices')
        #Get DJI Title
        SPTitle=[]
        for title in priceTable[0].find_all('th' , class_ = 'bb'):
            SPTitle.append(title.contents[0].strip('\n'))

        #Get DJI List
        SPList = []
        for child in priceTable[0].find_all('tr'):
            temp = []
            for child1 in child.find_all('td'):
                temp.append(child1.contents[0].strip(',').strip('\n').replace(',', ''))

            if temp != []:
                SPList.append(temp)
        #Save to file
        file = open(filePath+'SPList', 'w', encoding='utf-8')
        flag = 0
        for title in SPTitle:
            if flag !=0:
                file.write(',')
            else:
                flag=flag+1
            file.write(title)
        file.write('\n')
        for items in SPList:
            flag = 0
            for item in items:
                if flag == 0:
                    date = item.split(' ')
                    month = datetime.strptime(date[0],"%b").strftime('%m')
                    if len(date[1]) == 1:
                        date[1] = '0' + date[1]
                    day =  datetime.strptime(date[1],"%d").strftime('%d')
                    year = date[2]
                    file.write(year+'-'+month+'-'+day)
                    flag = 1
                else:
                    file.write(',')
                    file.write(item)

            file.write('\n')
        file.close()

        print(url)
    except:
        return 0

def parseStock(date,stockNum,type):
    try:
        searchDateTime = datetime.strptime(date,"%Y/%m/%d").strftime("%Y-%m-%d")
        with open(filePath+str(stockNum)) as f:
            reader = csv.reader(f)
            isTitleFlag = 0
            for row in reader:
                if isTitleFlag == 0:
                    isTitleFlag = 1
                else:
                    #(row[0])
                    if searchDateTime == row[0]:
                        return row[type]

        return 0

    except:
        print("Date:"+str(date) + " Type:" + str(type)  + " StockNum:" +str(stockNum)+" Parse Stock Error")
        return 0

