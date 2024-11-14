from bs4 import BeautifulSoup
import requests
import io
import pdfplumber
import polars as pl
import xlsxwriter


#This script will scrape the USDA website for the most recent food plans and return the weekly and monthly cost of each plan


def foodPlansmain():
    '''
    This function scrapes the USDA website for the most recent food plans and returns the weekly and monthly cost of each plan

    These food plans are at a federal level, so it doesn't change for different counties.

    The function returns @fused_df, a polars dataframewith the following columns:
        Cohorts	
        Age	
        Age Cohort	
        Thrifty Monthly	
        Low Monthly	M
        Moderate Monthly	
        Liberal Monthly
        
    Representing the monthly costs for different food plans divided by age group and cohort
    '''
    foodPlansHomePage = 'https://www.fns.usda.gov/cnpp/usda-food-plans-cost-food-monthly-reports'
    rSoup = requests.get(foodPlansHomePage)

    #raw web data
    soup = BeautifulSoup(rSoup.text, 'html.parser')

    #The table containing all pdfs with food plans
    tableSoup = soup.find('tbody')

    #The first row of the table contains the most recent food plan
    firstRow = tableSoup.find('tr')

    #First row is always federal thrifty, and second is always federal low-liberal
    thriftyPlanRaw = firstRow.find('a')
    lowToLiberalPlanRaw = thriftyPlanRaw.find_next_sibling('a')



    #Links to most recent plan pdfs
    
    linkToThriftyPlan = f"https://www.fns.usda.gov{thriftyPlanRaw['href']}"
    linkToLowLiberalPlan = f"https://www.fns.usda.gov{lowToLiberalPlanRaw['href']}"



    #Most recent food plan data
    #See comment below for more info
    print('Getting Food Plan Cost data....')
    
    thrifthy_plan = pl.DataFrame(getThriftyTable(linkToThriftyPlan))
    low_to_lib_plan = getLowLiberalTable(linkToLowLiberalPlan)

    

    '''
    getThriftyTable and getLowLiberalTable return polars dataframes with the following columns:

        getThriftyTable:
            Age-sex group, Weekly cost, Monthly cost

        getLowLiberalTable:
            Age-sex group, Weekly cost low, Weekly cost moderate, Weekly cost liberal, 
            Monthly cost low, Monthly cost moderate, Monthly cost liberal

    Columns can be referenced as dictionary keys, so for example, to print the weekly cost of the thrifty plan you do:
        print(thrifthy_plan['Weekly cost'])

    And you can also get the nth value of a column by using its index:
        print(thrifthy_plan['Weekly cost'][0]) 
  
    '''
    #print(thrifthy_plan)
    
    
    
    
    fused_df = fuse_food_plans(thrifthy_plan, low_to_lib_plan)
    #means_df = getAgeCohortMeans(fused_df)
    print('Done!')
    
    #print(low_to_lib_plan)
    
    return fused_df


 

def getThriftyTable(linkToThriftyPlan):
    #Thirfty plan to raw text
    
    '''
    This function takes a link to the most recent thrifty plan and returns a polars DataFrame with the following columns:

        Age-sex group, Weekly cost, Monthly cost

    Columns can be referenced as dictionary keys, so for example, to print the weekly cost of the thrifty plan you do:
        print(thrifthy_plan['Weekly cost'])

    And you can also get the nth value of a column by using its index:
        print(thrifthy_plan['Weekly cost'][0]) 

    '''
    rPDF = requests.get(linkToThriftyPlan)
    f = io.BytesIO(rPDF.content)
    
    with pdfplumber.open(f) as pdf:
        first_page = pdf.pages[0]
        tables = first_page.extract_tables()
    
    thirftyTableGroupSingle = splitGroupList1(tables[0][1][0])
    thirftyTableWeeklySingle = splitCostList1(tables[0][1][1])
    thirftyTableMonthlySingle = splitCostList1(tables[0][1][2])

    #thirftyTableGroupFamily = tables[0][2][0]
    thirftyTableWeeklyFamily = splitCostList1(tables[0][2][1])
    thirftyTableMonthlyFamily = splitCostList1(tables[0][2][2])
    
    #ageGroups = ['Child'] * 5 + ["Male"] * 5 + ["Female"] * 5 + ["Family"]
      
    thrifty_df = pl.DataFrame({
        # 'Cohorts': ageGroups,
        # 'Age' : thirftyTableGroupSingle + ['Reference Family'],
        # 'Weekly cost' : thirftyTableWeeklySingle + thirftyTableWeeklyFamily,
        # 'Monthly cost' : thirftyTableMonthlySingle + thirftyTableMonthlyFamily
        
        'Age' : thirftyTableGroupSingle ,
        'Weekly cost' : thirftyTableWeeklySingle ,
        'Monthly cost' : thirftyTableMonthlySingle
    })


    return thrifty_df

def getLowLiberalTable(linkToLowLiberalPlan):
      #Low to Liberal plan to raw text
    '''
    This function takes a link to the most recent low-liberal plan and returns a polars DataFrame with the following columns:

        Age, Weekly cost low, Weekly cost moderate, Weekly cost liberal, 
        Monthly cost low, Monthly cost moderate, Monthly cost liberal

    Columns can be referenced as dictionary keys, so for example, to print the weekly low cost of the moderate plan you do:
        print(low_to_liberaldf['Weekly cost low'])

    And you can also get the nth value of a column by using its index:
        print(low_to_liberaldf['Weekly cost low'][0]) 

    '''
    rPDF = requests.get(linkToLowLiberalPlan)
    f = io.BytesIO(rPDF.content)
    
    with pdfplumber.open(f) as pdf:
        first_page = pdf.pages[0]
        tables = first_page.extract_tables()
    
    # Split the values into groups:
    age_gender_groups = splitGroupList1(tables[0][1][0])
    weekly_low = splitCostList1(tables[0][1][1])
    weekly_moderate = splitCostList1(tables[0][1][2])
    weekly_liberal = splitCostList1(tables[0][1][3])
    monthly_low = splitCostList1(tables[0][1][4])
    monthly_moderate = splitCostList1(tables[0][1][5])
    monthly_liberal = splitCostList1(tables[0][1][6])

    
    low_to_liberaldf = pl.DataFrame({
        'Age': age_gender_groups,
        'Weekly cost low': weekly_low,
        'Weekly cost moderate': weekly_moderate,
        'Weekly cost liberal': weekly_liberal,
        'Monthly cost low': monthly_low,
        'Monthly cost moderate': monthly_moderate,
        'Monthly cost liberal': monthly_liberal
    })

    return low_to_liberaldf

   

    
def splitCostList1(numberList):
 
    """
    Split a string of numbers with dollar signs into a list of floats.
    
    Parameters
    ----------
    numberList : str
        A string of numbers with dollar signs, separated by newlines.
    
    Returns
    -------
    list
        A list of floats.
    
    Examples
    --------
    >>> splitCostList1('$7.80\n$8.90')
    [7.8, 8.9]
    """
    values = numberList.replace('$', '').split('\n')
    float_values = [float(value) for value in values]
        
    return float_values 


def splitGroupList1(groupList):
    """
    Splits a string of age group labels into a list of individual age ranges.

    Parameters
    ----------
    groupList : str
        A string containing age group labels separated by newlines, with an "Individual" label at the start.

    Returns
    -------
    list
        A list containing age ranges for child, male, and female groups, excluding headers.

    Examples
    --------
    >>> splitGroupList1('Individuals\nChild Header\nChild 1\nChild 2\n...') 
    ['Child 1', 'Child 2', ...']
    """
    values = groupList.split('\n')
        
    #Remove the "Individual" label
    values = values[1:]
    
    # removing headers (Child, Male, Female)
    child_ages = values[1:6]
    male_ages = values[7:12]
    female_ages = values[13:]

    # Create a 2D array
    food_plan_header = child_ages+male_ages+female_ages

    return food_plan_header


def fuse_food_plans(thrifthy_plan, low_to_lib_plan):
    
    """
    Fuse two DataFrames from the thrifty and low-to-liberal food plans into one.

    Parameters
    ----------
    thrifthy_plan : polars.DataFrame
        A DataFrame with columns 'Age', 'Weekly cost', and 'Monthly cost' for the thrifty plan.
    low_to_lib_plan : polars.DataFrame
        A DataFrame with columns 'Age', 'Weekly cost low', 'Weekly cost moderate', 'Weekly cost liberal', 'Monthly cost low', 'Monthly cost moderate', and 'Monthly cost liberal' for the low-to-liberal plan.

    Returns
    -------
    polars.DataFrame
        A DataFrame with columns 'Cohorts', 'Age', 'Age Cohort', 'Thrifty Monthly', 'Low Monthly', 'Moderate Monthly', and 'Liberal Monthly'.
    """
    ageGroups = ['Child'] * 5 + ["Male"] * 5 + ["Female"] * 5
    categories = ["Infant", "Preschooler", "Preschooler", "School Age", "School Age", "School Age", "Teenager", "Adult", "Senior", "Senior", "School Age", "Teenager", "Adult", "Senior", "Senior"]

    
    
    #print(low_to_lib_plan)
        
    fusedDF = pl.DataFrame({
        'Cohorts': ageGroups,
        'Age': low_to_lib_plan["Age"],
        'Age Cohort': categories,
        'Thrifty Monthly' : thrifthy_plan["Monthly cost"],
        'Low Monthly' : low_to_lib_plan["Monthly cost low"],
        'Moderate Monthly' : low_to_lib_plan["Monthly cost moderate"],
        'Liberal Monthly' : low_to_lib_plan["Monthly cost liberal"]
    })
    #print(fusedDF)
    
    #meansDF = getAgeCohortMeans(fusedDF)

    return fusedDF

def getAgeCohortMeans(df):
    """
    Calculate the mean of each food plan for each age group.

    Parameters
    ----------
    df : polars.DataFrame
        A DataFrame with columns 'Age', 'Age Cohort', 'Thrifty Monthly', 'Low Monthly', 'Moderate Monthly', and 'Liberal Monthly' for the fused food plans.

    Returns
    -------
    polars.DataFrame
        A DataFrame with columns 'Age Cohort', 'Thrifty', 'Low', 'Moderate', and 'Liberal' with the mean of each food plan for each age group.
    """
    print('Calculating food plan means...')
    meansDF = pl.DataFrame({})
    
    #The default order of the intialage cohort rows is the one below, but we'll need to change it later to be compatible with the Self Sufficiency Standard
    #Could change to doing the final order from the beggining but this makes it more readable
    
    categories = ["Infant", "Preschooler", "School Age", "Teenager", "Adult", "Senior"]

    
    for category in categories:
        mean = df.filter(pl.col('Age Cohort') == category).select(['Age Cohort','Thrifty Monthly', 'Low Monthly', 'Moderate Monthly', 'Liberal Monthly']).mean()
        meansDF = meansDF.vstack(mean)


    meansDF = df.group_by('Age Cohort').agg(pl.col(['Thrifty Monthly', 'Low Monthly', 'Moderate Monthly', 'Liberal Monthly']).mean())      
    meansDF = meansDF.rename({
        'Thrifty Monthly': 'Thrifty',
        'Low Monthly': 'Low',
        'Moderate Monthly': 'Moderate',
        'Liberal Monthly': 'Liberal'
    })
    
    #Change the format of the columns to be compatible with the Self Sufficiency Standard
    
    #Pop Senior
    meansDF = meansDF.filter(pl.col('Age Cohort') != 'Senior')
    
    #The new order must be Adult(s)	Infant(s) Preshooler(s)	Schoolager(s) Teenager(s)
    adult_row = meansDF.filter(pl.col('Age Cohort') == 'Adult').select(pl.col('*'))
    infant_row = meansDF.filter(pl.col('Age Cohort') == 'Infant').select(pl.col('*'))
    preschooler_row = meansDF.filter(pl.col('Age Cohort') == 'Preschooler').select(pl.col('*'))
    schoolager_row = meansDF.filter(pl.col('Age Cohort') == 'School Age').select(pl.col('*'))
    teenager_row = meansDF.filter(pl.col('Age Cohort') == 'Teenager').select(pl.col('*'))
    
    meansDF = pl.concat([adult_row, infant_row, preschooler_row, schoolager_row, teenager_row])
    
    #meansDF = meansDF.filter(pl.col('Age Cohort') != 'Adult')

    
    #meansDF = pl.concat([adult_row, meansDF])

      
   
    #print(meansDF)
    print('Done!')
    return meansDF

    

#foodPlansmain()
