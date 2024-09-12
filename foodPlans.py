from bs4 import BeautifulSoup
import requests
import io
import pdfplumber

#This script will scrape the USDA website for the most recent food plans and return the monthly cost of each plan


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


    #Links to the most recent food plans
    linkToThriftyPlan = f"https://www.fns.usda.gov{thriftyPlanRaw['href']}"

    '''
    getThriftyTable returns a 3D array such that:
    Index 0 is a 2D array of the child values
    Index 1 is a 2D array of the male values
    Index 2 is a 2D array of female values
    Index 3 is a 2D array of the reference family values 
    '''
    getThriftyTable(linkToThriftyPlan)
    
    
    linkToLowLiberalPlan = f"https://www.fns.usda.gov{lowToLiberalPlanRaw['href']}"




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

    # food_plan_costs_single returns a value [x,y,z] where: x is the age-sex group, y is the weekly cost, and z is monthly cost
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
    thirftyTableWeeklyFamily = splitCostList2(tables[0][2][1])
    thirftyTableMonthlyFamily = splitCostList2(tables[0][2][2])
    
    # Index 0 is the header, 1 is the weekly cost, 2 is monthly cost
    food_plan_costs_family = ['Reference Family', thirftyTableWeeklyFamily, thirftyTableMonthlyFamily]
    

    
    thrifty_divided =  [child_values, male_values ,female_values, food_plan_costs_family ]

    return thrifty_divided


    
def splitCostList1(numberList):
    values = numberList.replace('$', '').split('\n')
    float_values = [float(value) for value in values]
        
    return float_values 

def splitCostList2(numberList):
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
