from selenium import webdriver
from bs4 import BeautifulSoup
import polars as pl

# Set up selenium
url = 'https://www.bls.gov/emp/tables/education-and-training-by-occupation.htm'
driver = webdriver.Chrome()
driver.get(url)

# Get the table
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find('table', {'class': 'regular'})

# Extract the data
df = pl.DataFrame()

# Extract data from the table and create a DataFrame
header = []
data = []
max_length = 0

for row in table.find_all('tr'):
    elements_in_row = row.find_all(['td', 'th'])
    elements_in_row = [element.text.strip() for element in elements_in_row if element.text.strip()]
    
    if not header:
        header = elements_in_row
    else:
        max_length = max(max_length, len(elements_in_row))
        data.append(elements_in_row)

# Pad rows with empty values if necessary
for i, row in enumerate(data):
    data[i] += [''] * (max_length - len(row))

df = pl.DataFrame(data, schema=header)



# Deletes the last row (Its the sources of the info)
df = df.head(-1)

# Delete the last column (its links to a pdf)
df = df.drop(df.columns[-1])


print(df)

