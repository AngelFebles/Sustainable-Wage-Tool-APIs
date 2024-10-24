from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import Chrome, ChromeOptions
import os
from bs4 import BeautifulSoup
import polars as pl
import time






def dowload_job_salary_data():
    '''
    BLS is very strick with bot activity and automatic data scraping. 
    It prevents using tools like raw Beautiful Soup to download files.
    
    To go around this, we are going to open an instance of Chrome using Selenium and simulate user activity in the page to download a file.   
    '''
    
    url = 'https://download.bls.gov/pub/time.series/oe/'
    
    
    # Since we are downloading throught Chrome, files would normaly go to whatever download path you currently have.
    # The code below gets the absolute path of /DataFiles to change the download path there.
    
    raw_files_dir = os.path.join(os.path.dirname(__file__), '../DataFiles')
    absolute_path = os.path.abspath(raw_files_dir)
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
        print('Downloading job data...')
        #driver.find_element(By.XPATH, "//a[@href=\"/pub/time.series/oe/oe.data.1.AllData\"]").click()
        time.sleep(1)
        
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        
        # Wait until file is downloaded before closing chrome
        file_path = os.path.join(absolute_path, 'oe.data.1.AllData')
        while not os.path.exists(file_path):
            print('Waiting for download to finish...')
            time.sleep(1)
            
        
        
        driver.quit()
    print(file_path)
    df = file_to_df(file_path)
    
        
    #return file_to_df(absolute_path)



def file_to_df(path):
    raw_df = pl.read_csv(path, separator="\t")
    raw_df = raw_df.drop(raw_df.columns[-1])
    
    #print(raw_df)
    
    #os.remove(path)
    return raw_df

    
dowload_job_salary_data()