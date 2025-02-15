# Import necessary libraries
import openpyxl
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

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
df['Age'] = df['Age'].astype('category')

# Eliminate cyrillic characters
# Ensure df is a copy to avoid modifying a slice
df = df.copy()

# Process all columns except the last one
for c in df.columns[1:-1]:  # Loop through the appropriate columns
    # Remove text after the first parenthesis, then convert to category
    df[c] = df[c].apply(lambda x: str(x).split(" (")[0] if isinstance(x, str) else str(x))
    df[c] = df[c].astype('category')  # Convert to category

# Check summary statistics
df.describe()
# Include categorical columns
df.describe(include=['category'])

# Statistical analysis
# Count of unique values
df['Age'].value_counts()
# Count of unique values in percentage
df['Age'].value_counts(normalize=True)

# Sorting values
df.sort_values(by=['Age', 'Gender'], ascending=[True, False]).head()

# Data transformation
# Obtain information about gender value counts
df['Gender'].value_counts()
# Find unique values
df['Gender'].value_counts().keys()
# Average temperature for women
df[df['Gender'] == 'Female ']['Maximum body temperature'].mean()
# Average temperature for men
df[df['Gender'] == 'Male ']['Maximum body temperature'].mean()
# Statistics by gender
df.groupby(['Gender'])['Maximum body temperature'].describe()

# Pivot tables
# Age group by gender
pd.crosstab(df['Age'], df['Gender'])
# Summary information for body temperature by gender and age group
pd.pivot_table(df, values= 'Maximum body temperature', index= ['Age'], columns=['Gender'], aggfunc='mean', margins=True)


# Data visualization
# Number of surveyed men and women by age group
df = df.dropna(subset=['Age', 'Gender']) 
sns.countplot(x='Age', hue='Gender', data=df)

# Survey dynamic during research
df_numeric = df.select_dtypes(exclude=['category'])  # Keep only numeric columns
df_numeric.resample('1D').sum().plot()

# Temperature distribution of surveyed people that were sure or not sure to have had COVID-19
_, axes = plt.subplots(1, 2, sharey=True, figsize=(16,6))

df_t = df[df['Have you had Covid`19 this year?'] == 'Yes'].dropna(subset=['Maximum body temperature'])
sns.distplot(df_t['Maximum body temperature'], ax=axes[0])
df_t = df[df['Have you had Covid`19 this year?'] == 'Maybe'].dropna(subset=['Maximum body temperature'])
sns.distplot(df_t['Maximum body temperature'], ax=axes[1])