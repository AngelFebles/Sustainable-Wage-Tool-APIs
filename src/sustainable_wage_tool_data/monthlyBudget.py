import polars as pl

"""
      This is the last sheet to be generated in the output excel file.
      
      It adds up the costs from all other sheets to determine the monthly budget for each family type.
"""


def monthlyBudgetMain(sssDf, housingDF):
    """
    This function takes the Self Sufficiency Standard DataFrame and the Housing Costs DataFrame to generate
    the monthly budget for different family types and housing plans.

    It also takes into account the different food plans and their costs. (From foodPlans.py)

    The function returns a Polars DataFrame with the monthly budget for each family type and housing plan.

    The monthly budget includes the costs of the housing plan, the food plan, and other costs such as broadband and cell phone, health care costs,
    transportation costs, and taxes. The function also subtracts the earned income tax credit, the child care tax credit, and the child tax credit from the monthly budget.

    Parameters
    ----------
    sssDf : Polars DataFrame
        The Self Sufficiency Standard DataFrame, which contains the monthly costs for each family type and housing plan.
    housingDF : Polars DataFrame
        The Housing Costs DataFrame, which contains the costs of each housing plan.

    Returns
    -------
    Polars DataFrame
        A Polars DataFrame with the monthly budget for each family type and housing plan.

    """

    monthlyBudgetDf = pl.DataFrame()
    print("Getting Monthly Budget data....")

    initial_df = sssDf.select(pl.col(list(sssDf.columns)[:6])).fill_null(0)
    initial_df = initial_df.with_columns(
        [sssDf["Broadband & Cell Phone"].alias("Broadband & Cell Phone")]
    )
    initial_df = initial_df.with_columns(
        [sssDf["Health Care Costs "].alias("Health Care Costs ")]
    )
    initial_df = initial_df.with_columns(
        [sssDf["Transportation Costs"].alias("Transportation Costs")]
    )
    initial_df = initial_df.with_columns(
        [sssDf["Child Care Costs"].alias("Child Care Costs")]
    )
    initial_df = initial_df.with_columns([sssDf["Taxes"].alias("Taxes")])
    initial_df = initial_df.with_columns(
        [sssDf["Earned Income Tax Credit (-)"].alias("Earned Income Tax Credit (-)")]
    )
    initial_df = initial_df.with_columns(
        [sssDf["Child Care Tax Credit (-)"].alias("Child Care Tax Credit (-)")]
    )
    initial_df = initial_df.with_columns(
        [sssDf["Child Tax Credit (-)"].alias("Child Tax Credit (-)")]
    )

    foodPlans = ["Thrifty", "Low", "Moderate", "Liberal"]

    # For every housing plan, copy the whole family types table
    for housingType, housingCost in zip(
        housingDF["Type"].to_list(), housingDF["Cost"].to_list()
    ):
        for foodPlan in foodPlans:

            temp_df = initial_df.with_columns(
                [
                    pl.Series("Housing Selection", [housingType] * len(initial_df)),
                    pl.Series("Housing Costs", [housingCost] * len(initial_df)),
                ]
            )

            temp_df = temp_df.with_columns(
                [
                    pl.Series("Food Selection", [foodPlan] * len(initial_df)),
                    # pl.Series("Food Costs", getFoodCosts(len(initial_df)))
                ]
            )
            monthlyBudgetDf = (
                monthlyBudgetDf.vstack(temp_df) if len(monthlyBudgetDf) > 0 else temp_df
            )

        # pl.Series("Food Costs", getFoodCosts(len(initial_df)))

    monthlyBudgetDf = monthlyBudgetDf.with_columns(
        [pl.Series("Food Costs", getFoodCosts(len(monthlyBudgetDf)))]
    )

    monthlyBudgetDf = monthlyBudgetDf.with_columns(
        [pl.Series("Monthly Budget", calculateMonthlyBudget(len(monthlyBudgetDf)))]
    )

    # print(monthlyBudgetDf)

    # monthlyBudgetDf = getRestOfColumns(monthlyBudgetDf, sssDf)

    return monthlyBudgetDf


def getFoodCosts(listLength):
    """
    This function takes a list length and returns a list of formulas for calculating the food costs column in the monthly budget dataframe.

    The formulas are based on the food means table and the housing selection, food selection, and family type columns in the monthly budget dataframe.

    Parameters
    ----------
    listLength : int
        The length of the list to be returned.

    Returns
    -------
    list
        A list of formulas for calculating the food costs column in the monthly budget dataframe.
    """
    foodCostsList = []

    # This is an excel formula to calculate the monthly costs
    # Code just adds the formula for each row, changing the elements used for the formula as needed

    current_row = 2
    while current_row < listLength + 2:
        food_formula = f"""=(HLOOKUP('Monthly Budget'!Q{current_row},Food_means!$A$1:$E$6,2,FALSE)*'Monthly Budget'!$B{current_row}) + (HLOOKUP('Monthly Budget'!Q{current_row},Food_means!$A$1:$E$6,3,FALSE)*'Monthly Budget'!$C{current_row}) + (HLOOKUP('Monthly Budget'!Q{current_row},Food_means!$A$1:$E$6,4,FALSE)*'Monthly Budget'!$D{current_row}) + (HLOOKUP('Monthly Budget'!Q{current_row},Food_means!$A$1:$E$6,5,FALSE)*'Monthly Budget'!$E{current_row}) + (HLOOKUP('Monthly Budget'!Q{current_row},Food_means!$A$1:$E$6,6,FALSE)*'Monthly Budget'!$F{current_row})"""
        foodCostsList.append(food_formula)
        current_row += 1

    return foodCostsList


def calculateMonthlyBudget(listLength):

    # =SUM(G2:N2,P2,R2)
    monthlyBudgetList = []
    current_row = 2

    while current_row < listLength + 2:
        monthlyBudgetFormula = (
            f"""=SUM(G{current_row}:N{current_row},P{current_row},R{current_row})"""
        )
        monthlyBudgetList.append(monthlyBudgetFormula)
        current_row += 1

    return monthlyBudgetList


# def getRestOfColumns(monthlyBudgetDf, sssDf):
