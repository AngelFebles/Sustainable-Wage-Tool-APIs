import requests

APIKEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI2IiwianRpIjoiN2EwOGVjZWQyOTc4NGUzNGE3YzNiNWU0YjgyZTEyMWJlYzk3MzZhMmM5YjExMDRjM2Q0NjQ1NDFiZjBmMTM4MDMzMGE3ZjMxNmNjYjNiZGQiLCJpYXQiOjE3MjU1NjA2OTUuOTY3NDUxLCJuYmYiOjE3MjU1NjA2OTUuOTY3NDUzLCJleHAiOjIwNDEwOTM0OTUuOTYyNjAzLCJzdWIiOiI3NzI3MyIsInNjb3BlcyI6W119.PC5tJhuUKPf0LDMADlgADvWzJR16y2xTWOi-S2pWUrBy25P3fMWQTabtuPe8xKfYzuxApEYv8wvVbBHHdPt8yQ'
countyCode = '5510199999'  # Racine, WI MSA
year = 2025

#FY 2024 Racine, WI MSA FMTs for All Bedroom Sizes
#Deleting year property defaults to 2025's predictions
url = f'https://www.huduser.gov/hudapi/public/fmr/data/{countyCode}?year={year}'

headers = {
    'Authorization': f'Bearer {APIKEY}'
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

