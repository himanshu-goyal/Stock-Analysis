import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("C:\Users\himan\Downloads\Salaries.csv", index_col = 'Id')
del df['EmployeeName']
del df['Agency']
del df['Notes']

print(df.Status.unique())
#We have nan, so replace it with NA
df['Status'].fillna("NA", inplace=True)
print(df.Status.unique())

print(df.isnull().sum())
df['Benefits'].fillna(0,inplace=True)
df= df[df.JobTitle != 'Not provided']
df.dropna(inplace=True)
print(df.isnull().sum())
df.head()

#this will produce the data from histogram
#plotting histogram for salaries for year 2014
year_2014 = df['Year'] == 2014
income_2014 = df[year_2014]['TotalPayBenefits']
income_2014.to_csv("C:\Users\himan\Downloads\data-hist.csv", header=True)

#print(df)

df.head()
year_counts = df.groupby('Year').mean()
year_counts.to_csv("C:\Users\himan\Downloads\data-line.csv", header=True)