from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import Chrome, ChromeOptions
import os
from bs4 import BeautifulSoup
import polars as pl
import time




#BLS is very strick with bot activity and automatic data scraping.
#Selenium + BeautifulSoup is slower than just vanilla BeautifulSoup, but without Selenium BLS will block all requests.

def get_education_requirements():
    # Set up selenium
    url = 'https://www.bls.gov/emp/tables/education-and-training-by-occupation.htm'
    driver = webdriver.Chrome()
    driver.get(url)

    # Get the table
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', {'class': 'regular'})

    # Extract the data
    df_education_requirements = pl.DataFrame()

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

    df_education_requirements = pl.DataFrame(data, schema=header)



    # Deletes the last row (Its the sources of the info)
    df_education_requirements = df_education_requirements.head(-1)

    # Delete the last column (its links to a pdf_education_requirements)
    df_education_requirements = df_education_requirements.drop(df_education_requirements.columns[-1])


    return df_education_requirements

def get_occupation_salary(absolute_path):
    url = 'https://jobcenterofwisconsin.com/WisConomy/SaveSearch/RetriveSearchquery/1529'
    
    prefs = {
    "download.default_directory": absolute_path,
    "download.directory_upgrade": True,
    "download.prompt_for_download": False,
    }

    chromeOptions = ChromeOptions()
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = Chrome(options=chromeOptions)
    
    driver.get(url)
    time.sleep(1)

    try:
        # Find the button with the ID 'button_GenerateReport', then click it
        generateReportButton = driver.find_element(By.ID, 'button_GenerateReport').click()
        print("Report generated successfully!")
        # Wait for the report to be generated
        time.sleep(1)
        
        # Find the anchor with the href '#Download'
        pressDownloadButton1 = driver.find_element(By.XPATH, "//a[@href='#Download']").click()
        print("Changed page")
        time.sleep(1)
        #Press final download button
        pressDownloadButton2 = driver.find_element(By.XPATH, "//button[@id='button_Download']").click()

        
        
        time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()
   
        
def fuse_tables(edutable, occupationtable):
    
    print("a")
        
    

raw_files_dir = os.path.join(os.path.dirname(__file__), '../rawFiles')
absolute_path = os.path.abspath(raw_files_dir)

get_occupation_salary(absolute_path)
 

