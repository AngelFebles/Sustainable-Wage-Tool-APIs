import polars as pl
import xlsxwriter

from scripts.foodPlans import foodPlansmain
from scripts.foodPlans import getAgeCohortMeans
from scripts.housingCost import housingCostMain
from scripts.selfSufficiencyStandard import sssMain

housing_cost_plan_df = pl.DataFrame(housingCostMain())
food_plans_df = pl.DataFrame(foodPlansmain())
food_plans_means_df = pl.DataFrame(getAgeCohortMeans(food_plans_df))
self_sufficiency_standard_df = pl.DataFrame(sssMain())


#thrifthydf.write_excel(workbook="polars_simple.xlsx", worksheet='foodPlansA')

with xlsxwriter.Workbook("dataOutput.xlsx") as workbook:
    housing_cost_plan_df.write_excel(workbook=workbook,worksheet='Housing_lookup')
    self_sufficiency_standard_df.write_excel(workbook=workbook,worksheet='Self_Sufficiency_Standard')
    food_plans_df.write_excel(workbook=workbook,worksheet='Food_lookup')
    food_plans_means_df.write_excel(workbook=workbook,worksheet='Food_means')