# Import necessary libraries
import openpyxl
import pandas as pd
from datetime import datetime

# Load data from repository
df = pd.read_excel(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/data-science-in-health-care-basic-statistical-analysis/COVID_19.xlsx",
    "Sheet1",
)
print(df.head())


# Function to transform date to datetime
def parse(x):
    y = x.split()
    t = y[1][:8]
    z = y[0] + " " + t
    d = datetime.strptime(z, "%Y-%m-%d %H:%M:%S")
    return d


# Reload data
df = pd.read_excel(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/data-science-in-health-care-basic-statistical-analysis/COVID_19.xlsx",
    "Sheet1",
    na_values="NaN",
    parse_dates=["Date time"],
    index_col=0,
    date_parser=parse,
)

#Data preparation
# Drop null values for gender column
df = df.dropna(subset=["Gender"])
# Change yes/no values
d = {"No": False, "Yes": True}
c = "Do you vaccinated influenza?"
df.loc[:, c] = df[c].map(d)
# Overview of dataset
df.info()
# Change column type
c = "Age"
df.loc[:, c] = df[c].astype("category")
# Eliminate cyrillic characters
# Ensure df is a copy to avoid modifying a slice
df = df.copy()

# Process all columns except the last one
for c in df.columns[:-1]:  # Exclude the last column
    df.loc[:, c] = df[c].astype(str).apply(lambda x: x.split(" (")[0])  # Remove text inside parentheses
    df.loc[:, c] = df[c].astype("category")

# Check summary statistics
df.describe()
# Include categorical columns
df.describe(include=['category'])

