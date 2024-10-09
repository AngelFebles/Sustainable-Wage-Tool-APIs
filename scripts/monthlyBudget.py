import polars as pl


def monthlyBudgetMain(sssDf, housingDF,foodDF):
    monthlyBudgetDf = pl.DataFrame({})
    print('Getting Monthly Budget data....')
    
    formula = '''=(HLOOKUP('Monthly Budget'!I2,Food_means!$A$1:$E$6,2,FALSE)*'Monthly Budget'!$B2) + (HLOOKUP('Monthly Budget'!I2,Food_means!$A$1:$E$6,3,FALSE)*'Monthly Budget'!$C2) + (HLOOKUP('Monthly Budget'!I2,Food_means!$A$1:$E$6,4,FALSE)*'Monthly Budget'!$D2) + (HLOOKUP('Monthly Budget'!I2,Food_means!$A$1:$E$6,5,FALSE)*'Monthly Budget'!$E2) + (HLOOKUP('Monthly Budget'!I2,Food_means!$A$1:$E$6,6,FALSE)*'Monthly Budget'!$F2)'''

    initial_df = sssDf.select(pl.col(list(sssDf.columns)[:6])).fill_null(0)
    
 
    monthlyBudgetDf = pl.DataFrame({
        'Family Type': [],
        'Adult(s)': [],
        'Infant(s)': [],
        'Preshooler(s)': [],
        'Schoolager(s)': [],
        'Teenager(s)': [],
        'Housing Selection': [],
        'Housing Costs': [],
        # 'Food Selection': [],
        # 'Food Costs': [],
        # 'Technology Costs': [],
        # 'Health Care Costs': [],
        # 'Transportation Costs': [],
        # 'Child Care Costs': [],
        # 'Taxes': [],
        # 'Earned Income Tax Credit (-)': [],
        # 'Child Care Tax Credit (-)': [],
        # 'Child Tax Credit (-)': [],
    })
    
    #monthlyBudgetDf = pl.DataFrame({})
    #monthlyBudgetDf = monthlyBudgetDf.with_columns(pl.Series("Housing Selection", [""] * len(monthlyBudgetDf)))   
     
    for row in housingDF['Type']:
        #row_df = initial_df.clone()
        initial_df = initial_df.with_columns(pl.Series("Housing Selection", [row] * len(initial_df)))
        if len(monthlyBudgetDf) == 0:
            monthlyBudgetDf = initial_df
        else:
            monthlyBudgetDf = monthlyBudgetDf.vstack(initial_df)
    
        
                
    
  

    print(monthlyBudgetDf)
    
    return monthlyBudgetDf
    


