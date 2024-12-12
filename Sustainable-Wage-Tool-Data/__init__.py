import polars as pl
import xlsxwriter

import argparse

from scripts.foodPlans import foodPlansmain
from scripts.foodPlans import getAgeCohortMeans
from scripts.housingCost import housingCostMain
from scripts.selfSufficiencyStandard import sssMain
from scripts.monthlyBudget import monthlyBudgetMain
from scripts.jobDataScrapeSEL import jobDataScrapeStarter
#from scripts.employmentDataScrape import get_employement_data



"""
This is the starter script for the project.
It calls all the other scripts and outputs the data to an excel file. -> dataOutput.xlsx
It also outputs an excel file with job data (salaries, educational requirements, ...) -> jobData.xlsx

dataOutput.xlsx contains the following sheets:

Housing_lookup  --- Costs for each housing plan
Self_Sufficiency_Standard --- Self Sufficiency Standard data
Food_lookup --- Costs for each food plan, divided by age and gender
Food_means --- Average costs for each food plan, divided by age group (Adult, Infant, Preschooler, School Age, Teenager)
Monthly Budget --- Addition of all the previous costs to determine the monthly budget according to family size


jobData.xlsx contains the following sheets:

Job_Data --- Misc data for each job (annual wage, hourly wage, number of jobs available, ...)
Education_Requirements --- Educational requirements for each job

"""


# Legacy code, if you want to hardcode county data for debugging:

# # For the SSS, this is the FIPS code of the county followed by five 9s.
# # You can get the FIPS code from here:
# # https://dpi.wi.gov/sfs/statistical/basic-facts/wisconsin-counties
# # So for example, Sauk County has has a FIPS code of 55111, so you would put 5511199999
# # Racine has a FIPS code of 55101, so you would put 5510199999, etc
# countyCode_HousingCost = '5510199999'  

# # Make sure to put county name with the first letter beging a capital letter 
# # Followed by the word "County" (wich also needs to have leading capital letter )
# # For example: "Racine County", "Dodge County", "Eau Claire County"
# county_SelfSufficiencyStandard = 'Racine County'


# #Make sure to put county name with the first letter beging a capital letter
# #Then, followed by the string ", WI" (For Wisconsin) (there is no space between county name and the comma)
# #For example: "Racine, WI", "Dodge, WI", "Eau Claire, WI"
# county_JobData = 'Racine, WI'

def generate_county_data(county_name):

    #This capitalizes the first letter of each word in the county name and 
    #makes the other letters lowercase
    #The "du" expection is for the county "Fond du Lac", which needs du to be lowercase
    county_name = county_name.title().replace("Du", "du")

    """
    Fip codes are unique identifiers for states, counties, etc

    Since codes are static, is faster to store the ones from all counties of Wisconsin in a file
    rather than looking them up from an api every time.

    TODO: If this code is to be used for other states, this dictionary will need to be updated.
    
    Got these from here: https://dpi.wi.gov/sfs/statistical/basic-facts/wisconsin-counties
    
    """
   
    counties_fips_path = 'Sustainable-Wage-Tool-Data/DataFiles/countiesFIPSCodes.data'
    
    # Read the file into a DataFrame
    counties_fips_df = pl.read_csv(counties_fips_path, separator="\t")
        
    # Find the FIPS code for the given county name
    county_row = counties_fips_df.filter(pl.col("County Name") == county_name.capitalize())
    fips_code = county_row.select("FIPS Code").to_series().item()
    
    if not fips_code:
        raise ValueError("County not found")
    
    #We need to append 5 9s to the end of the FIPS code to lookup in the database
    county_code_housing_cost = f'{fips_code}99999'
      
    county_self_sufficiency_standard = f'{county_name.capitalize()} County'
    county_job_data = f'{county_name.capitalize()}, WI'
    
    return county_code_housing_cost, county_self_sufficiency_standard, county_job_data



parser = argparse.ArgumentParser(description="Process county name for data extraction.")
parser.add_argument('county_name', type=str, help='Name of the county to process')
args = parser.parse_args()

countyCode_HousingCost, county_SelfSufficiencyStandard, county_JobData = generate_county_data(args.county_name)



#Creating dataframes for each sheet

housing_cost_plan_df = pl.DataFrame(housingCostMain(countyCode_HousingCost))
food_plans_df = pl.DataFrame(foodPlansmain())
food_plans_means_df = pl.DataFrame(getAgeCohortMeans(food_plans_df))
self_sufficiency_standard_df = pl.DataFrame(sssMain(county_SelfSufficiencyStandard))
monthly_budget_df = pl.DataFrame(monthlyBudgetMain(self_sufficiency_standard_df,housing_cost_plan_df))

#thrifthydf.write_excel(workbook="polars_simple.xlsx", worksheet='foodPlansA')


#Filling the dataframes with the info from each script

with xlsxwriter.Workbook("dataOutput.xlsx") as workbook:
    housing_cost_plan_df.write_excel(workbook=workbook,worksheet='Housing_lookup')
    self_sufficiency_standard_df.write_excel(workbook=workbook,worksheet='Self_Sufficiency_Standard')
    food_plans_df.write_excel(workbook=workbook,worksheet='Food_lookup')
    food_plans_means_df.write_excel(workbook=workbook,worksheet='Food_means')    
    #jobs_data_df.write_excel(workbook=workbook,worksheet='Jobs')
    monthly_budget_df.write_excel(workbook=workbook,worksheet='Monthly Budget')
    

jobDataScrapeStarter(county_JobData)
print("Done!")