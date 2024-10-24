from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import Chrome, ChromeOptions
import os
from bs4 import BeautifulSoup
import polars as pl
import time


#Change with your county name, it pulls data from the oe.area file.
county = 'Racine, WI'


def get_county_id(county):
    
    job_data_files_dir = os.path.join(os.path.dirname(__file__), '../JobDataFiles/oe.area')
    absolute_pathJD = os.path.abspath(job_data_files_dir)
    
       
    #oe.area
    counties_df = pl.read_csv(absolute_pathJD, separator="\t")
    
    
    # Look for the row containing the string county in the last column
    county_row = counties_df.filter(pl.col(counties_df.columns[-1]) == county)
    
    # Extract the value from the 'area_code' column for the matched county row
    county_area_code = county_row.select('area_code').to_series().item()

    return county_area_code





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
    #print(file_path)
    df = file_to_df(file_path)
    
        
    #return file_to_df(absolute_path)

def split_df(df):
    county_id = get_county_id(county)
    
    df_only_from_county = df.filter(pl.col('series_id                     ').str.contains(county_id))
    
    return df_only_from_county


def file_to_df(path):
    raw_df = pl.read_csv(path, separator="\t")
    #drop the "comments" column
    raw_df = raw_df.drop(raw_df.columns[-1])
 
    df_only_from_county = split_df(raw_df)
    
    
       #take the column with all the data
    df_only_from_county_only_data = pl.DataFrame({
        "values": df_only_from_county.select(pl.col(df_only_from_county.columns[-1]))
    })
    
        #jobIDs
    df_only_from_county_onlyIDS = pl.DataFrame({
        "values": df_only_from_county.select(pl.col(df_only_from_county.columns[0]))
    })
    
    print(df_only_from_county_onlyIDS)
    
        
    # Assuming your original DataFrame is named 'df'
    original_column = df_only_from_county_only_data.to_series().to_numpy()

    # Calculate the number of complete rows in the new DataFrame
    num_complete_rows = len(original_column) // 17

    # Reshape the array
    reshaped_array = original_column[:num_complete_rows * 17].reshape(-1, 17)

    # Create column names
    column_names = [f"col_{i}" for i in range(1, 18)]

    # Create the new DataFrame
    new_df = pl.DataFrame(reshaped_array, schema=column_names)

    print(new_df.shape)
    print(new_df)
    
    return new_df    
    #print(df_only_from_county_only_data)
    
    # new_columns = {f"col_{i}": df["values"].slice(i, 1) for i in range(17)}

    # df_transformed = pl.DataFrame(new_columns)

    # print(df_transformed)


    
    #print(df)
    
    #os.remove(path)
    

    
    #return raw_df

    
dowload_job_salary_data()

