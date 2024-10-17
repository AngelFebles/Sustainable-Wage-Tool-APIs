from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import polars as pl

# Set up selenium
url = 'https://www.bls.gov/emp/tables/education-and-training-by-occupation.htm'
driver = webdriver.Chrome()
driver.get(url)

# Get the table
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('table', {'class': 'regular'})

# Extract the data
df = pd.DataFrame()

for row in table.find_all('tr'):
    columns = row.find_all(['td', 'th'])
    columns = [elementsInRow.text.strip() for elementsInRow in columns]
    df = df._append(pd.Series(columns), ignore_index=True) 

#Makes first row the column names
df.columns = df.iloc[0]
df = df.iloc[1:]

#Deletes the last row (Its the sources of the info)
df = df.iloc[:-1]

#Deletes the last column (Its links to a pdf)
df = df.iloc[:, :-1]


print(df)

