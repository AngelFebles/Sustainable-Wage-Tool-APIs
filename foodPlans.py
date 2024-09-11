from bs4 import BeautifulSoup
import requests
import io
import PyPDF2

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
lowToLowLiberalPlanRaw = thriftyPlanRaw.find_next_sibling('a')


#Links to the most recent food plans
linkToThriftyPlan = f"https://www.fns.usda.gov{thriftyPlanRaw['href']}"
linkToLowLiberalPlan = f"https://www.fns.usda.gov{lowToLowLiberalPlanRaw['href']}"


print(linkToThriftyPlan)

#Thirfty plan to rar text
rPDF = requests.get(linkToThriftyPlan)
f = io.BytesIO(rPDF.content)

reader = PyPDF2.PdfReader(f)
contents = reader.pages[0].extract_text()

print(contents)