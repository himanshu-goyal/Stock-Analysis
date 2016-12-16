import urllib2
import numpy as np
from sklearn import linear_model
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
df1=[]
def RetrieveTrainingData(stockSymbols,days):
    tempRow = []
    temp=[]
    urllib2.urlopen("http://api.kibot.com/?action=login&user=guest&password=guest")
    url = "http://api.kibot.com/?action=history&symbol=" + stockSymbols + "&interval=daily&period=" + str(days) +"&unadjusted=1&regularsession=1"
    apiData = urllib2.urlopen(url).read().replace('\r','').split("\n")
    for row in apiData:
        if(len(row) > 0):
            tempRow = row.split(',')
            temp.append(tempRow)
    df1 = pd.DataFrame(temp, columns= ['date','OpenPrice','HighPrice', 'LowPrice','ClosePrice','Volume'])
    df1['date'] = pd.to_datetime(df1['date'])
    df1['date'] = pd.to_datetime(df1['date'], format='%Y-%m-%d')
    df1.set_index(['date'], inplace=True)
    df1 = df1.astype(float)
    return df1
del df1[:]
def PlotNormalizedOpeningPrice(symbols,days):
    stockSymbol= []
    stockSymbol= symbols.split(',')
    startDate= datetime.today().date() - timedelta(days)
    endDate= datetime.today()
    dates= pd.date_range(startDate,endDate)
    df2= pd.DataFrame(index=dates)
    for symbol in stockSymbol:
        df= RetrieveTrainingData(symbol,days)
        df= df['OpenPrice']
        df= df/ df.ix[0,:]
        df2 = df2.join(df)
        df2 = df2.rename(columns={'OpenPrice':symbol})
        df2 = df2.dropna()
    df2.plot()
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Normalized OpenPrice price', fontsize=10)
    plt.show()
    
def CalculateDailyReturns(symbols,days):
    stockSymbol= []
    stockSymbol= symbols.split(',')
    startDate= datetime.today().date() - timedelta(days)
    endDate= datetime.today()
    dates= pd.date_range(startDate,endDate)
    df2= pd.DataFrame(index=dates)
    for symbol in stockSymbol:
        df= RetrieveTrainingData(symbol,days)
        df= df['ClosePrice']
        dailyReturn = df.copy()    
        dailyReturn[1:]= (df[1:]/df[:-1].values) - 1
        dailyReturn.ix[0,0]=0   
        df2 = df2.join(dailyReturn)
        df2 = df2.rename(columns={'ClosePrice':symbol})
        df2 = df2.dropna()
        mean1 = df2.mean()
        std1 = df2.std()
    df2.plot()
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Daily Returns', fontsize=10)
    plt.show()
    return df2
def plotHistogram(symbols,days):
    df= CalculateDailyReturns(symbols,days)
    i=len(df.columns)
    names = df.columns.values
    print(names[0])
    print(names[1])
    for n in range(0,i):
        if(n< (i+1)):
            df[names[n]].hist(bins=40,label=names[n])
    plt.legend(loc="upper right")        
    plt.show()    
    
def CalculateMean(symbols,days):
    stockSymbol= []
    stockSymbol= symbols.split(',')
    startDate= datetime.today().date() - timedelta(days)
    endDate= datetime.today()
    dates= pd.date_range(startDate,endDate)
    df2= pd.DataFrame(index=dates)
    for symbol in stockSymbol:
        df= RetrieveTrainingData(symbol,days)
        df= df['ClosePrice']
        dMean = df.copy()     
        df2 = df2.join(dMean)
        df2 = df2.rename(columns={'ClosePrice':symbol})
        df2 = df2.dropna()
    for symbol in stockSymbol:
        ax = df2[symbol].plot(title="Bollinger Band Plot for " +symbol, label='Price')
        rm= pd.rolling_mean(df2[symbol], window=40)
        rs= pd.rolling_std(df2[symbol], window=40)
        upperBand=rm + rs*2
        lowerBand=rm - rs*2
        upperBand.plot(label='Upper band', ax=ax)
        lowerBand.plot(label='Lower band', ax=ax)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend(loc='Upper left')
        plt.show()
        rm=0
        rs=0
        upperBand=0
        lowerBand=0
    mean1 = df2.mean()
    std1 = df2.std()
    print(mean1)
    print(std1)
    return