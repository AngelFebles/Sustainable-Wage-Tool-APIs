import requests
import scripts.credentials as credentials
import polars as pl


def housingCostMain():

    df = ''
    
    countyCode = '5510199999'  # Racine, WI MSA

    #FY Racine, WI MSA FMTs for All Bedroom Sizes
    url = f'https://www.huduser.gov/hudapi/public/fmr/data/{countyCode}'

    headers = {
        'Authorization': f'Bearer {credentials.APIKEYHOUSING}'
    }

    response = requests.get(url, headers=headers)
    
    print('Getting Housing Cost data....')

    if response.status_code == 200:
        data = response.json().get('data').get('basicdata')
        df = pl.DataFrame({
            'Efficiency': [data.get('Efficiency')],
            'One-Bedroom': [data.get('One-Bedroom')],
            'Two-Bedroom': [data.get('Two-Bedroom')],
            'Three-Bedroom': [data.get('Three-Bedroom')],
            'Four-Bedroom': [data.get('Four-Bedroom')]
        })

        
        #print(df)
        
        print("Done!")
        return df
       
    else:
        print('Housing Cost API request failed with status code:', response.status_code)
        
        


#housingCostMain()