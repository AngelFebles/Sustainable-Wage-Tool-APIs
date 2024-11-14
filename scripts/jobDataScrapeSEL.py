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

    county_header = 'OEUM00' + str(county_id)
    print(county_header)

    df_only_from_county = df.filter(pl.col('series_id                     ').str.contains(county_header))
    
    return df_only_from_county


def file_to_df(path):
    raw_df = pl.read_csv(path, separator="\t")
    #drop the "comments" column
    raw_df = raw_df.drop(raw_df.columns[-1])
    
    #Remove front and back characters (series identifiers) so we only have duplicates of the job id
    
    raw_df = raw_df.with_columns(pl.col("series_id                     ").str.slice(4,).alias("idCounty"))
    raw_df = raw_df.with_columns(pl.col("idCounty").str.head(-19).alias("idCounty"))

    #print(raw_df)
   
    df_only_from_county = split_df(raw_df)
    
    #take the column with all the data
    df_only_from_county_only_data = pl.DataFrame({
        "values": df_only_from_county.select(pl.col(df_only_from_county.columns[-2]))
    })

    
    #jobIDs
    df_only_from_county_onlyIDS = pl.DataFrame({
        "ids": df_only_from_county.select(pl.col(df_only_from_county.columns[0]))
    })
    
    # print('A')
    # print(df_only_from_county_only_data)
    
    #print(df_only_from_county_onlyIDS)
    
        
    
    """
    The list returns everything in a single column.
    
    We need to reshape and redistribute the elements into the 17 respective categories of each job
    
    We also need to have a single jobID per job, as oposed to 1 jobid per each job caterogry
    """
    
    ######Reshaping data######
    
    original_column = df_only_from_county_only_data.to_series().to_numpy()

    # Calculate the number of complete rows in the new DataFrame
    num_complete_rows = len(original_column) // 17

    # Reshape the array
    reshaped_array = original_column[:num_complete_rows * 17].reshape(-1, 17)

    # Create column names
    column_names = [f"col_{i}" for i in range(1, 18)]

    # Create the new DataFrame
    reshaped_df = pl.DataFrame(reshaped_array, schema=column_names)


    #print(df_only_from_county_onlyIDS)
    
    ######Creating jobIDs######
    #print(df_only_from_county_onlyIDS)
    #Remove front and back characters (series identifiers) so we only have duplicates of the job id
    df_only_from_county_onlyIDS = df_only_from_county_onlyIDS.with_columns(
    pl.col("ids").str.head(-7).alias("ids"))

    df_only_from_county_onlyIDS = df_only_from_county_onlyIDS.with_columns(
    pl.col("ids").str.tail(-17).alias("ids"))

    #print(df_only_from_county_onlyIDS)
    # print('B')
    # print(df_only_from_county_onlyIDS)
    
    #Delete duplicates of jobIDs
    df_only_from_county_onlyIDS = df_only_from_county_onlyIDS.unique(subset="ids",maintain_order=True)
    
   



    #print(df_only_from_county_onlyIDS)
    
    

    combined_df = pl.concat([df_only_from_county_onlyIDS, reshaped_df], how="horizontal")
    combined_df = combined_df.rename({
        "col_1": "Employment",
        "col_2": "Employment percent relative standard error",
        "col_3": "Hourly mean wage",
        "col_4": "Annual mean wage",
        "col_5": "Wage percent relative standard error",
        "col_6": "Hourly 10th percentile wage",
        "col_7": "Hourly 25th percentile wage",
        "col_8": "Hourly median wage",
        "col_9": "Hourly 75th percentile wage",
        "col_10": "Hourly 90th percentile wage",
        "col_11": "Annual 10th percentile wage",
        "col_12": "Annual 25th percentile wage",
        "col_13": "Annual median wage",
        "col_14": "Annual 75th percentile wage",
        "col_15": "Annual 90th percentile wage",
        "col_16": "Employment per 1,000 jobs",
        "col_17": "Location Quotient"
    })
    




    print(combined_df)
    
   # print(combined_df)
    
    
    
    #print(df_only_from_county_onlyIDS)
    
    #return combined_df    
    
    

    
    #print(df)
    
    #os.remove(path)
    

    
    #return raw_df

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

    df_education_requirements = pl.DataFrame(data, schema=header, orient="row")



    # Deletes the last row (Its the sources of the info)
    df_education_requirements = df_education_requirements.head(-1)

    # Delete the last column (its links to a pdf_education_requirements)
    df_education_requirements = df_education_requirements.drop(df_education_requirements.columns[-1])


    return df_education_requirements


    
dowload_job_salary_data()
print(get_education_requirements())

