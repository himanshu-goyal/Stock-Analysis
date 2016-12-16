import urllib2
import numpy as np
from sklearn import linear_model
import datetime
import matplotlib.pyplot as plt
dates= []
historicalPrices = []
def RetrieveTrainingData(stockSymbols,days):
    #clear any data from the lists
    del dates[:]
    del historicalPrices[:]
    tempLine = []
    urllib2.urlopen("http://api.kibot.com/?action=login&user=guest&password=guest")
    url = "http://api.kibot.com/?action=history&symbol=" + stockSymbols + "&interval=daily&period="+ str(days) +"&unadjusted=1&regularsession=1"
    apiData = urllib2.urlopen(url).read().split("\n")
    for line in apiData:
        if(len(line) > 0):
            tempLine = line.split(',')
            price = tempLine[1]
            date1 = tempLine[0]
            date1 = date1[3:5]
            historicalPrices.append(float(price))
            dates.append(int(date1))
    return historicalPrices,dates
def PredictPriceAndShowPlot(symbols, futureDate,days):
    a= futureDate
    stockSymbol = []
    stockSymbol = symbols.split(',')
    for symbol in stockSymbol:
        print(symbol)
        RetrieveTrainingData(symbol,days)
        linear_mod= linear_model.LinearRegression()
        dates1= np.reshape(dates, (len(dates),1))
        historicalPrices1= np.reshape(historicalPrices, (len(historicalPrices),1))
        linear_mod.fit(dates1,historicalPrices1,1)
        futurePrice= linear_mod.predict(a)
        print("Future opening price for stock: ", symbol, "is ", str(futurePrice))
        plt.scatter(dates1,historicalPrices1, color='yellow')
        plt.plot(dates1,linear_mod.predict(dates1), color='blue', linewidth=1)
        plt.show()
    return
