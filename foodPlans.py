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
    #Thirfty plan to rar text
    rPDF = requests.get(linkToThriftyPlan)
    f = io.BytesIO(rPDF.content)
    
    with pdfplumber.open(f) as pdf:
        first_page = pdf.pages[0]
        tables = first_page.extract_tables()
    
    thirftyTableGroup1 =  splitGroupList(tables[0][1][0])
    thirftyTableWeeklySingle =  splitCostList(tables[0][1][1])
    thirftyTableMonthlySingle = splitCostList(tables[0][1][2])
    
    thirftyTableGroup2 = tables[0][2][0]
    thirftyTableWeeklyFamily = splitCostList(tables[0][2][1])
    thirftyTableMonthlyFamily = splitCostList(tables[0][2][2])
    
    print(thirftyTableGroup1)
    
def splitCostList(numberList):
    values = numberList.replace('$', '').split('\n')
    float_values = [float(value) for value in values]
    
    return float_values 

def splitGroupList(groupList):
    values = groupList.split('\n')
    return values
    
main()
