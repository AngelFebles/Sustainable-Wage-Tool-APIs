import requests
from bs4 import BeautifulSoup
import polars as pl
import re

url = 'https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents#Table'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', {'class': 'wikitable sortable'})
rows = table.find_all('tr')

counties = []
for row in rows[1:]:
    cols = row.find_all('td')
    county = {
        'name': cols[0].text.strip()
    }
    counties.append(county)


words = []
for county in counties:
    name = county['name']
    separated_words = re.findall(r'\b\w+\b', name)
    words.extend(separated_words)

lowercase_words = [word for word in words if re.match(r'^[a-z]', word)]
#lowercase_words = (set(lowercase_words))

lowercase_words = list(set(lowercase_words))

print(lowercase_words)

print(">>> splitCostList1('$7.80\\n$8.90')")

# county_name = 'racine'

# articles = ['the', 't', 'e', 'u', 'l', 'ab', 'a', 'r', 'z', 'of', 'v', 'j', 'i', 'and', 'n', 'aa', 'g', 'm', 'y', 's', 'f', 'k', 'p', 'qui', 'h', 'x', 'du', 'd', 'q', 'w', 'o']

# words = county_name.split()
# new_words = []

# for word in words:
#     if word.lower() in [article.lower() for article in articles]:
#         new_words.append(word.lower())
#     else:
#         new_words.append(word.title())
# county_name = ' '.join(new_words)

# print(county_name)
