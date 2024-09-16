import requests
import credentials

countyCode = '5510199999'  # Racine, WI MSA

#FY Racine, WI MSA FMTs for All Bedroom Sizes
url = f'https://www.huduser.gov/hudapi/public/fmr/data/{countyCode}'

headers = {
    'Authorization': f'Bearer {credentials.APIKEYHOUSING}'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json().get('data').get('basicdata')

    housingEfficiency = data.get('Efficiency')
    housingOneBedroom = data.get('One-Bedroom')
    housingTwoBedroom = data.get('Two-Bedroom')
    housingThreeBedroom = data.get('Three-Bedroom')
    housingFourBedroom = data.get('Four-Bedroom')
    
    print(data)
else:
    print('API request failed with status code:', response.status_code)

