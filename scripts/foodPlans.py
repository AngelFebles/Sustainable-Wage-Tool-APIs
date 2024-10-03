from bs4 import BeautifulSoup
import requests
import io
import pdfplumber
import polars as pl
import xlsxwriter


#This script will scrape the USDA website for the most recent food plans and return the weekly and monthly cost of each plan


def foodPlansmain():
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
    values = numberList.replace('$', '').split('\n')
    float_values = [float(value) for value in values]
        
    return float_values 


def splitGroupList1(groupList):
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

    meansDF = pl.DataFrame({})
    categories = ["Infant", "Preschooler", "School Age", "Teenager", "Adult", "Senior"]

    for category in categories:
        mean = df.filter(pl.col('Age Cohort') == category).select(['Age Cohort','Thrifty Monthly', 'Low Monthly', 'Moderate Monthly', 'Liberal Monthly']).mean()
        meansDF = meansDF.vstack(mean)

    meansDF = df.group_by('Age Cohort').agg(pl.col(['Thrifty Monthly', 'Low Monthly', 'Moderate Monthly', 'Liberal Monthly']).mean())        
   
    #print(meansDF)

    return meansDF

    

foodPlansmain()
