from bs4 import BeautifulSoup
import requests
import io
import PyPDF2
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
    food_plan_costs_single = []
    for i in range(len(thirftyTableGroupSingle)):
        group = thirftyTableGroupSingle[i]
        week = thirftyTableWeeklySingle[i]
        month = thirftyTableMonthlySingle[i]
        food_plan_costs_single.append([group, week, month])

    print(food_plan_costs_single[3])
    

    

    #print(food_plan_costs_single)
  
    
    thirftyTableGroupFamily = tables[0][2][0]
    thirftyTableWeeklyFamily = splitCostList2(tables[0][2][1])
    thirftyTableMonthlyFamily = splitCostList2(tables[0][2][2])
    
    # Index 0 is the header, 1 is the weekly cost, 2 is monthly cost
    #food_plan_costs_family = [thirftyTableGroupFamily, thirftyTableWeeklyFamily, thirftyTableMonthlyFamily]
    #  print(food_plan_costs_family)
    
    #print(thirftyTableMonthlyFamily)
    
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
    
    # Split the values into groups: Child, Male, Female
    child_values = values[1:6]
    male_values = values[7:12]
    female_values = values[13:]

    # Create a 2D array
    food_plan_header = child_values+male_values+female_values

    return food_plan_header
    

    
main()
