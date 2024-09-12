from bs4 import BeautifulSoup
import requests
import io
import pdfplumber

#This script will scrape the USDA website for the most recent food plans and return the weekly and monthly cost of each plan


def main():
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
    thrifthy_plan_ARR = getThriftyTable(linkToThriftyPlan)
    low_to_lib_plan_ARR = getLowLiberalTable(linkToLowLiberalPlan)


    '''
    getThriftyTable and getLowLiberalTable return 3D arrays such that:
    Index 0 is a 2D array of the child values
    Index 1 is a 2D array of the male values
    Index 2 is a 2D array of female values
    Index 3 is a 2D array of the reference family values --- (Only applicable to getThriftyTable)


    
    -------Array Structure--------
    
    [TRHIRFTY PLAN]
    The statement:
    print(thrifthy_plan_ARR[0]) (Which returns the child values, check above table for reference)

    Could return these example 2D array:
    [['child 1 year', 25.3, 109.6], ['child 2-3 years', 38.0, 164.7],  ... ]
    Where for each sub-array [x,y,z] : 

    x is the age-sex group
    y is the weekly cost
    z is monthly cost

    [LOW TO LIBERAL PLAN]

    The statement:
    print(low_to_lib_plan_ARR[1]) (Which returns the male values, check above table for reference)

    Could return these example 2D array:
    [['male 12-13 years', 69.6, 86.2, 101.0, 301.5, 373.7, 437.4], ...]

    Where for each sub-array [a,b,c,d,e,f,g] :
    a is the age-sex group
    b is the weekly cost for low plan
    c is the weekly cost for moderate plan
    d is the weekly cost for liberal plan
    e is the monthly cost for low plan
    f is the monthly cost for moderate plan
    g is the monthly cost for liberal plan
    '''

 

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

    # food_plan_costs_single returns an array [x,y,z] where: x is the age-sex group, y is the weekly cost, and z is monthly cost
    thrifty_plan_costs_single = []
    for i in range(len(thirftyTableGroupSingle)):
        group = thirftyTableGroupSingle[i]
        week = thirftyTableWeeklySingle[i]
        month = thirftyTableMonthlySingle[i]
        thrifty_plan_costs_single.append([group, week, month])
    
      # Split the values into groups: Child, Male, Female
    child_values = thrifty_plan_costs_single[0:5]
    male_values = thrifty_plan_costs_single[5:10]
    female_values = thrifty_plan_costs_single[10:]  
    
    #thirftyTableGroupFamily = tables[0][2][0]
    thirftyTableWeeklyFamily = splitCostList1(tables[0][2][1])
    thirftyTableMonthlyFamily = splitCostList1(tables[0][2][2])
    
    # Index 0 is the header, 1 is the weekly cost, 2 is monthly cost
    food_plan_costs_family = ['Reference Family', thirftyTableWeeklyFamily, thirftyTableMonthlyFamily]
    

    
    thrifty_divided =  [child_values, male_values ,female_values, food_plan_costs_family ]

    return thrifty_divided

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


    low_to_liberal_raw = []
    for i in range(len(age_gender_groups)):
        names = age_gender_groups[i]
        weekLo = weekly_low[i]
        weekM = weekly_moderate[i]
        weekLi = weekly_liberal[i]
        monthLo = monthly_low[i]
        monthM = monthly_moderate[i]
        monthLi = monthly_liberal[i]
        
        low_to_liberal_raw.append([names, weekLo, weekM, weekLi, monthLo, monthM, monthLi])
    
      # Split the values into groups: Child, Male, Female
    child_values = low_to_liberal_raw[0:5]
    male_values = low_to_liberal_raw[5:10]
    female_values = low_to_liberal_raw[10:]
    
    low_to_liberal_Final = [child_values, male_values, female_values]

    return low_to_liberal_Final

   

    
def splitCostList1(numberList):
    values = numberList.replace('$', '').split('\n')
    float_values = [float(value) for value in values]
        
    return float_values 


def splitGroupList1(groupList):
    values = groupList.split('\n')
    
    #Remove the "Individual" label
    values = values[1:]
    
    # Adding headers (Child, Male, Female)
    child_ages = [f"child {value}" for value in values[1:6]]
    male_ages = [f"male {value}" for value in values[7:12]]
    female_ages = [f"female {value}" for value in values[13:]]

 

    # Create a 2D array
    food_plan_header = child_ages+male_ages+female_ages

    return food_plan_header
    

    
main()
