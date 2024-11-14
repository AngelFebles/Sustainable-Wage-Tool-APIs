import requests
import scripts.credentials as credentials
import polars as pl


def housingCostMain():

    """
    Scrapes the HUD website to retrieve the most recent housing cost data for Racine, WI by default.
    
    TODO: parameterize county code. var @countyCode at line 27
    
    The function sends a GET request to the HUD API to fetch data for different bedroom sizes.
    If successful, it processes the JSON response into a Polars DataFrame containing housing costs
    for Efficiency, One-Bedroom, Two-Bedroom, Three-Bedroom, and Four-Bedroom types.
    
    Returns:
        @df: A polars DataFrame with three columns, 'Type', 'Lookup', and 'Cost', representing housing costs for each type.
    
    Prints a message if the request fails, including the status code of the response.
    """
    
    
    df = ''
    
    #Variable to parameterize
    countyCode = '5510199999'  # Racine, WI MSA

    #Website with prices for All Bedroom Sizes for the specified county
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
        
        #year = data.get('year')
    
        
        print("Done!")
        
        #The format of the table from the website is flipped, so we need to transpose (make columns into rows and rows into columns)
        #Code would still work without this step but it makes the output look nicer
        
        df = df.transpose(include_header=True).with_row_index()
        df = df.rename({"index": "Lookup", "column": "Type", "column_0": "Cost"})

        #print(df)
        return df
       
    else:
        print('Housing Cost API request failed with status code:', response.status_code)
        
        


#housingCostMain()
