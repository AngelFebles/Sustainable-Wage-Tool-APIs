import polars as pl
import xlsxwriter

from scripts.foodPlans import foodPlansmain
from scripts.housingCost import housingCostMain
from scripts.selfSufficiencyStandard import sssMain

housing_cost_plan_df = pl.DataFrame(housingCostMain())
thrifthy_plan_df = pl.DataFrame(foodPlansmain())
self_sufficiency_standard_df = pl.DataFrame(sssMain())


#thrifthydf.write_excel(workbook="polars_simple.xlsx", worksheet='foodPlansA')

with xlsxwriter.Workbook("dataOutput.xlsx") as workbook:
    housing_cost_plan_df.write_excel(workbook=workbook,worksheet='Housing_lookup')
    self_sufficiency_standard_df.write_excel(workbook=workbook,worksheet='Self_Sufficiency_Standard')
    thrifthy_plan_df.write_excel(workbook=workbook,worksheet='Food_lookup')