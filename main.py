#import necessary libraries
import openpyxl
import pandas as pd
from datetime import datetime
#data from repository
df = pd.read_excel(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/data-science-in-health-care-basic-statistical-analysis/COVID_19.xlsx',
    'Sheet1')
print(df.head)