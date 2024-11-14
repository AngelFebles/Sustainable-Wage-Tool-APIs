import polars as pl
import xlsxwriter

from scripts.foodPlans import foodPlansmain
from scripts.foodPlans import getAgeCohortMeans
from scripts.housingCost import housingCostMain
from scripts.selfSufficiencyStandard import sssMain
from scripts.monthlyBudget import monthlyBudgetMain
#from scripts.employmentDataScrape import get_employement_data



"""
This is the starter script for the project.
It calls all the other scripts and outputs the data to an excel file. -> dataOutput.xlsx

dataOutput.xlsx contains the following sheets:

Housing_lookup  --- Costs for each housing plan
Self_Sufficiency_Standard
Food_lookup --- Costs for each food plan, divided by age and gender
Food_means --- Average costs for each food plan, divided by age group (Adult, Infant, Preschooler, School Age, Teenager)


Monthly Budget --- Addition of all the previous costs to determine the monthly budget according to family size

"""



#Creating dataframes for each sheet

housing_cost_plan_df = pl.DataFrame(housingCostMain())
food_plans_df = pl.DataFrame(foodPlansmain())
food_plans_means_df = pl.DataFrame(getAgeCohortMeans(food_plans_df))
self_sufficiency_standard_df = pl.DataFrame(sssMain())
#jobs_data_df = pl.DataFrame(get_employement_data())
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