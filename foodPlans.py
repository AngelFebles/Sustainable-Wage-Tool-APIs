from bs4 import BeautifulSoup
import requests


foodPlansHomePage = 'https://www.fns.usda.gov/cnpp/usda-food-plans-cost-food-monthly-reports'
r = requests.get(foodPlansHomePage)

#raw web data
soup = BeautifulSoup(r.text, 'html.parser')

#The table containing all pdfs with food plans
tableSoup = soup.find('tbody')

#The first row of the table contains the most recent food plan
firstRow = tableSoup.find('tr')

#First row is always federal thrifty, and second is always federal low-liberal
thriftyPlanRaw = firstRow.find('a')
lowToLowLiberalPlanRaw = thriftyPlanRaw.find_next_sibling('a')


#Links to the most recent food plans
linkToThriftyPlan = f"https://www.fns.usda.gov{thriftyPlanRaw['href']}"
linkToLowLiberalPlan = f"https://www.fns.usda.gov{lowToLowLiberalPlanRaw['href']}"


print(linkToThriftyPlan)