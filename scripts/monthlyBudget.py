import polars as pl


def monthlyBudgetMain(sssDf, housingDF):
    monthlyBudgetDf = pl.DataFrame()
    print('Getting Monthly Budget data....')
    

    initial_df = sssDf.select(pl.col(list(sssDf.columns)[:6])).fill_null(0)
    initial_df = initial_df.with_columns([sssDf['Broadband & Cell Phone'].alias('Broadband & Cell Phone')])
    initial_df = initial_df.with_columns([sssDf['Health Care Costs '].alias('Health Care Costs ')])
    initial_df = initial_df.with_columns([sssDf['Transportation Costs'].alias('Transportation Costs')])
    initial_df = initial_df.with_columns([sssDf['Child Care Costs'].alias('Child Care Costs')])
    initial_df = initial_df.with_columns([sssDf['Taxes'].alias('Taxes')])
    initial_df = initial_df.with_columns([sssDf['Earned Income Tax Credit (-)'].alias('Earned Income Tax Credit (-)')])
    initial_df = initial_df.with_columns([sssDf['Child Care Tax Credit (-)'].alias('Child Care Tax Credit (-)')])
    initial_df = initial_df.with_columns([sssDf['Child Tax Credit (-)'].alias('Child Tax Credit (-)')])

    

    foodPlans = ['Thrifty', 'Low', 'Moderate', 'Liberal']
       
    #For every housing plan, copy the whole family types table
    for housingType, housingCost in zip(housingDF['Type'].to_list(), housingDF['Cost'].to_list()):
            for foodPlan in foodPlans:
             
                temp_df = initial_df.with_columns([
                    pl.Series("Housing Selection", [housingType] * len(initial_df)),
                    pl.Series("Housing Costs", [housingCost] * len(initial_df))
                ])
                
                temp_df = temp_df.with_columns([
                    pl.Series("Food Selection", [foodPlan] * len(initial_df)),
                    #pl.Series("Food Costs", getFoodCosts(len(initial_df)))
                ])
                monthlyBudgetDf = monthlyBudgetDf.vstack(temp_df) if len(monthlyBudgetDf) > 0 else temp_df
                
            #pl.Series("Food Costs", getFoodCosts(len(initial_df)))
                      
    monthlyBudgetDf = monthlyBudgetDf.with_columns([
        pl.Series("Food Costs", getFoodCosts(len(monthlyBudgetDf)))
    ])
            
    #print(monthlyBudgetDf) 
    
    #monthlyBudgetDf = getRestOfColumns(monthlyBudgetDf, sssDf)
        
    return monthlyBudgetDf

def getFoodCosts(listLength):

    foodCostsList = []
    
    current_row = 2
    while current_row < listLength+2:
            food_formula = f'''=(HLOOKUP('Monthly Budget'!Q{current_row},Food_means!$A$1:$E$6,2,FALSE)*'Monthly Budget'!$B{current_row}) + (HLOOKUP('Monthly Budget'!Q{current_row},Food_means!$A$1:$E$6,3,FALSE)*'Monthly Budget'!$C{current_row}) + (HLOOKUP('Monthly Budget'!Q{current_row},Food_means!$A$1:$E$6,4,FALSE)*'Monthly Budget'!$D{current_row}) + (HLOOKUP('Monthly Budget'!Q{current_row},Food_means!$A$1:$E$6,5,FALSE)*'Monthly Budget'!$E{current_row}) + (HLOOKUP('Monthly Budget'!Q{current_row},Food_means!$A$1:$E$6,6,FALSE)*'Monthly Budget'!$F{current_row})'''
            foodCostsList.append(food_formula)
            current_row += 1

    return foodCostsList


#def getRestOfColumns(monthlyBudgetDf, sssDf):
    
    