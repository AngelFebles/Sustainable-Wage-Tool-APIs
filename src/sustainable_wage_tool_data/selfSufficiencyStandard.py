import polars as pl
import requests
from bs4 import BeautifulSoup
import os

import xlsxwriter

def sssMain(county_SelfSufficiencyStandard):
    """
    Fetches the Self Sufficiency Standard data from the designated website for Wisconsin. 
    
    The function scrapes the website to find the most recent Self Sufficiency Standard file link,
    downloads it if not already present in the './DataFiles/' directory, and reads the file to extract data 
    specific to Racine County. The data is processed using the `readFile` function, which reads the file 
    into a Polars DataFrame.

    Returns:
       @dataFrame: A polars DataFrame with data specific to the County extracted from the Self Sufficiency Standard file.
    """
    print('Getting Self Sufficiency Standard data....')
    
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
    os.makedirs(r'src\sustainable_wage_tool_data\DataFiles', exist_ok=True)
    
    
    #Check if we already have that file
    file_path = os.path.join(r'src\sustainable_wage_tool_data\DataFiles', filename)

    #If not, download it
    if not os.path.exists(file_path):
        print('Downloading ', filename + '...')
        response = requests.get(linkToSSS)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print('Download complete!')
    else:
        print(f'{filename} already downloaded.')

    #readFile(file_path)
     
    return readFile(file_path, county_SelfSufficiencyStandard)
    

def readFile(file_path, county_SelfSufficiencyStandard):
    """
    Reads an Excel file using polars and extracts the Self Sufficiency Standard data.

    Parameters:
        file_path (str): The path to the Excel file.

    """
    print('Reading the file...')
    # Read the Excel file using polars
    #df = pl.read_excel(file_path, sheet_name='By County')
    df = pl.read_excel(file_path, sheet_name='By Family').with_row_index(name='index')


    # Get the id of the row that contains the county, Racine by default
    
    county = county_SelfSufficiencyStandard
    
    county_row = df.filter(pl.col(df.columns[10]).str.contains(county))
    county_index = county_row.select(pl.first()).row(0)[0]
    
    #Theres 719 rows for each county, thats where the upperbound comes from
    dataFrame = df[county_index:county_index+719]
    
    #To make the output cleaner, I deleted the index column
    dataFrame = dataFrame.drop(dataFrame.columns[0])

    
    #print(dataFrame)

    print('Done!')

    return dataFrame

        
#sssMain()
 






