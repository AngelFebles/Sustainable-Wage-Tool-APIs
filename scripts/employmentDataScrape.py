from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


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

def get_occupation_salary():
    driver = webdriver.Chrome()
    driver.get("https://data.bls.gov/oes/#/home")

    # Press "Multiple occupations for one geographical area"
    try:
        # Wait until the page has completely loaded
        WebDriverWait(driver, 30).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )
        print("Page fully loaded!")
        
        # Find first radial
        radio_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Multiple occupations for one geographical area"))
        )

        # Scroll into view and ensure the element is visible
        driver.execute_script("arguments[0].scrollIntoView(true);", radio_button)
        time.sleep(1)  # Give time for any scrolling or UI transitions

        # Click the first radio button
        driver.execute_script("arguments[0].click();", radio_button)
        print("First radio button clicked")
        
        # Wait for the second button to be available
        second_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Metropolitan or Non Metropolitan Area"))
        )
        
        # Scroll into view and ensure the element is visible
        driver.execute_script("arguments[0].scrollIntoView(true);", second_button)
        time.sleep(1)  # Give time for any scrolling or UI transitions

        # Click the second button
        driver.execute_script("arguments[0].click();", second_button)
        print("Second button clicked")

        # Wait for the <select> element with ID 'smsa' to appear
        smsa_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "smsa"))
        )
        
        print("Select element with ID 'smsa' found!")
       

        # Wait for a bit longer to ensure options are loaded
        time.sleep(3)  # Wait for options to load; adjust as necessary

        # Find the <optgroup> with the label "Wisconsin"
        optgroup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//optgroup[@label='Wisconsin']"))
        )
        #print(optgroup.get_attribute("innerHTML"))
        # Retrieve all <option> elements within the <optgroup>
        
        # Retrieve the <option> element with the label "Racine, WI"
        county_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//optgroup[@label='Wisconsin']/option[@label='Racine, WI']"))
        )
        # Select the county option
        driver.execute_script("arguments[0].click();", county_option)
        print("Racine, WI selected")
       
        
        
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()



# Call the function
get_occupation_salary()