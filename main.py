#import necessary libraries
import openpyxl
import pandas as pd
from datetime import datetime
#data from repository
df = pd.read_excel(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/data-science-in-health-care-basic-statistical-analysis/COVID_19.xlsx',
    'Sheet1')
print(df.head)
#function to transform date to datetime
def parse(x):
    y = x.split()
    t = y[1][:8]
    z=y[0] + " " + t
    d = datetime.strptime(z, '%Y-%m-%d %H:%M:%S')
    return d
#reload data
df = pd.read_excel(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/data-science-in-health-care-basic-statistical-analysis/COVID_19.xlsx',
    'Sheet1',
    na_values="NaN",
    parse_dates=['Date time'],
    index_col=0,
    date_format=parse)

#drop null values for gender column
df = df.dropna(subset=['Gender'])
#change yes/no values
d = {'No' : False, 'Yes' : True}
c = 'Do you vaccinated influenza?'
df.loc[:, c] = df[c].map(d)
#overview of dataset
df.info()
#change column type
c = 'Age'
df.loc[:, c] = df[c].astype('category')