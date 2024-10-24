import requests
import json
import polars as pl
import credentials


headers = {'Content-type': 'application/json'}
#data = json.dumps({"seriesid": ['OEUM003954000000023101104'], "registrationkey" : credentials.APIKEYJOBDB})

data = json.dumps({"seriesid":["OEUM003954000000053708117"], "registrationkey" : credentials.APIKEYJOBDB})

# "registrationkey" 

#data = json.dumps({"seriesid": ['OEUM003954000000000000001']})

#data = json.dumps({"seriesid": ['OEUS550000000000023101104']})

p = requests.post(f'https://api.bls.gov/publicAPI/v2/timeseries/data', data=data, headers=headers)
json_data = json.loads(p.text)


#df = pl.read_excel(p.content)

print(json_data)

