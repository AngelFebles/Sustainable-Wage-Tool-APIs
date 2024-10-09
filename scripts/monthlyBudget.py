import polars as pl


def monthlyBudgetMain(sssDf, housingDF,foodDF):
    monthlyBudgetDf = pl.DataFrame()
    print('Getting Monthly Budget data....')
    
    food_formula = '''=(HLOOKUP('Monthly Budget'!I2,Food_means!$A$1:$E$6,2,FALSE)*'Monthly Budget'!$B2) + (HLOOKUP('Monthly Budget'!I2,Food_means!$A$1:$E$6,3,FALSE)*'Monthly Budget'!$C2) + (HLOOKUP('Monthly Budget'!I2,Food_means!$A$1:$E$6,4,FALSE)*'Monthly Budget'!$D2) + (HLOOKUP('Monthly Budget'!I2,Food_means!$A$1:$E$6,5,FALSE)*'Monthly Budget'!$E2) + (HLOOKUP('Monthly Budget'!I2,Food_means!$A$1:$E$6,6,FALSE)*'Monthly Budget'!$F2)'''

    initial_df = sssDf.select(pl.col(list(sssDf.columns)[:6])).fill_null(0)
    
 
    # monthlyBudgetDf = pl.DataFrame({
    #     'Family Type': [],
    #     'Adult(s)': [],
    #     'Infant(s)': [],
    #     'Preshooler(s)': [],
    #     'Schoolager(s)': [],
    #     'Teenager(s)': [],
    #     'Housing Selection': [],
    #     'Housing Costs': [],
    #     'Food Selection': [],
    #     # 'Food Costs': [],
    #     # 'Technology Costs': [],
    #     # 'Health Care Costs': [],
    #     # 'Transportation Costs': [],
    #     # 'Child Care Costs': [],
    #     # 'Taxes': [],
    #     # 'Earned Income Tax Credit (-)': [],
    #     # 'Child Care Tax Credit (-)': [],
    #     # 'Child Tax Credit (-)': [],
    # })
    
    foodPlans = ['Thrifty', 'Low', 'Moderate', 'Liberal']
       
    #For every housing plan, copy the whole family types table

        
    for housingType, housingCost in zip(housingDF['Type'].to_list(), housingDF['Cost'].to_list()):
            for foodPlan in foodPlans:
                temp_df = initial_df.with_columns([
                    pl.Series("Food Selection", [foodPlan] * len(initial_df)),
                    #pl.Series("Food Costs", [foodDF[foodPlan].to_list()] * len(initial_df))
                ])
                temp_df = temp_df.with_columns([
                    pl.Series("Housing Selection", [housingType] * len(initial_df)),
                    pl.Series("Housing Costs", [housingCost] * len(initial_df))
                ])
                monthlyBudgetDf = monthlyBudgetDf.vstack(temp_df) if len(monthlyBudgetDf) > 0 else temp_df
                      
    print(monthlyBudgetDf)
        
    return monthlyBudgetDf


