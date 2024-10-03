import polars as pl
import requests
from bs4 import BeautifulSoup
import os

def sssMain():
    
    sssHomePage = 'https://selfsufficiencystandard.org/Wisconsin/'
    rSoup = requests.get(sssHomePage)

    #raw web data
    soup = BeautifulSoup(rSoup.text, 'html.parser')

    #The table containing all Self Sufficiency Standard files
    tableSoup = soup.find('div', {'data-id': '2cc978d4'})

    #The first li element contains the most recent Self Sufficiency Standard file
    tableSoup = tableSoup.find('li')
    linkToSSS = tableSoup.find('a')['href']

    
    # Extract the file name from the URL
    filename = os.path.basename(linkToSSS)

    # Create the directory if it doesn't exist
    os.makedirs('./rawFiles', exist_ok=True)
    
    
    #Check if we already have that file
    file_path = os.path.join('./rawFiles', filename)

    if not os.path.exists(file_path):
        print('Downloading ', filename + '...')
        # Download the file
        response = requests.get(linkToSSS)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print('Download complete!')
    else:
        print(f'{filename} already downloaded.')

   
    
    return readFile(file_path)
    

def readFile(file_path):
    print('Reading the file...')
    # Read the Excel file using polars
    #df = pl.read_excel(file_path, sheet_name='By County')
    df = pl.read_excel(file_path, sheet_name='By County').with_row_index(name='index')

    # 52 is Racine's county number in spreadsheet, 1 is a constant offset
    # offset = 52+1
    # print(df[1335-offset])

    # Get the id of the row that contains Racine County
    county_row = df.filter(pl.col(df.columns[1]).str.contains('Racine County'))
    county_index = county_row.select(pl.first()).row(0)[0]
    
    #After County header, there's 8 rows of padding before the first data row (Thats why first row in table is county_index+8)
    #Then there's 12 rows of data (thats why last row in table is county_index+20)
    
    monthlyCosts = df[county_index+8:county_index+20]
    
    selfSufficiencyWages = df[county_index+21:county_index+24]
    
    emergencySavings = df[county_index+24]
    
    new_df = pl.concat([monthlyCosts, selfSufficiencyWages, emergencySavings], rechunk=True)    
    
    print(new_df)
    
    return new_df

        
sssMain()
 






