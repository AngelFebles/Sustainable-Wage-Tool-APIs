from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import Chrome, ChromeOptions
import os
from bs4 import BeautifulSoup
import polars as pl
import time


def get_employement_data():
    print('Getting employment data...')
    
    educationDF = get_education_requirements()
    
    raw_files_dir = os.path.join(os.path.dirname(__file__), '../rawFiles')
    absolute_path = os.path.abspath(raw_files_dir)
    
    salaryDF = get_occupation_salary(absolute_path)

    # print(educationDF)
    # print(salaryDF)
    
    finalTable = fuse_tables(educationDF, salaryDF)
    
    return finalTable


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

    df_education_requirements = pl.DataFrame(data, schema=header, orient="row")



    # Deletes the last row (Its the sources of the info)
    df_education_requirements = df_education_requirements.head(-1)

    # Delete the last column (its links to a pdf_education_requirements)
    df_education_requirements = df_education_requirements.drop(df_education_requirements.columns[-1])


    return df_education_requirements

def get_occupation_salary(absolute_path):
    url = 'https://jobcenterofwisconsin.com/WisConomy/SaveSearch/RetriveSearchquery/1530'
    
    
    
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
        
    return file_to_df(absolute_path)
   
#Always outputs a .csv file, so we look for that one
def file_to_df(path):
    """
    Read all CSV files in the given directory into a DataFrame and delete the original files.

    Args:
        path (str): The path to the directory containing CSV files.

    Returns:
        list: List of DataFrames read from the CSV files.
    """
    if os.path.isdir(path):
        # Get all files in the directory
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        
        # Filter only the CSV files
        csv_files = [f for f in files if f.endswith('.csv')]
        
        # Read all CSV files into a DataFrame
        dfs = [pl.read_csv(os.path.join(path, file)) for file in csv_files]
        #print(dfs)

        # Delete the original files
        for file in csv_files:
            file_path = os.path.join(path, file)
            os.remove(file_path)

        return dfs
    else:
        print("File not found or not a CSV file")
        return None
def fuse_tables(edutable, occupationtable):
    # Check if occupationtable is a list and convert it to a DataFrame if necessary
    if isinstance(occupationtable, list):
        occupationtable = pl.DataFrame(occupationtable[0])
    
    if not isinstance(occupationtable, pl.DataFrame):
        raise ValueError("occupationtable must be a Polars DataFrame or convertible to one")
    
    # Convert the "Occupation Code" to string and clean up the data
    aDF = occupationtable.with_columns(
        pl.col("Occupation Code").cast(pl.Utf8).str.strip_chars()
    ).select(["Occupation Code", "Employment", "Mean Wages"])
    
    # Drop the last two columns of edutable and clean the code column
    edutable = edutable.drop(edutable.columns[-2:])
    col_name = edutable.columns[1]  # The 2023 National Employment Matrix code
    edutable = edutable.with_columns(
        pl.col(col_name).str.replace("-", "").str.strip_chars().alias(col_name)
    )
    
    # # Debugging: Check unique values before joining
    # print("Unique Occupation Codes in aDF:")
    # print(aDF.select("Occupation Code").unique())
    
    # print(f"Unique {col_name} in edutable:")
    # #print(edutable.select(col_name).unique())
    
    # Perform an inner join on the matching codes
    joined_df = edutable.join(
        aDF,
        left_on=col_name,
        right_on="Occupation Code",
        how="inner"
    )
    
    filtered_df = joined_df.filter(joined_df["Employment"] != "S")
    
    #print(joined_df)
    return filtered_df


#get_employement_data()