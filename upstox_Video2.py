#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import urllib.parse
import pandas as pd
import requests


# In[ ]:


apiKey = 'ncdjo9d8-8rjfm3-7jfue-89r3-7654326d'
secretKey = '7ndm0snth'
redirectUrl = 'https://127.0.0.1:5000/'
rurl = urllib.parse.quote('https://127.0.0.1:5000/',safe="")
rurl


# In[ ]:


uri = f'https://api-v2.upstox.com/login/authorization/dialog?response_type=code&client_id={apiKey}&redirect_uri={rurl}'
uri


# In[ ]:


url = 'https://api-v2.upstox.com/login/authorization/token'
code = 'Ub8cx_'
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'code': code,
    'client_id': apiKey,
    'client_secret': secretKey,
    'redirect_uri': redirectUrl,
    'grant_type': 'authorization_code'
}

response = requests.post(url, headers=headers, data=data)
json_response = response.json()

json_response


# In[ ]:


access_token = json_response['access_token']
access_token


# In[ ]:


url = 'https://api-v2.upstox.com/user/get-funds-and-margin'
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Authorization': f'Bearer {access_token}'
}
params = {
    'segment': 'COM'  #'COM'
}


response = requests.get(url, headers=headers, params=params)
response.json()


# In[ ]:





# In[ ]:


fileUrl ='https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz'
symboldf = pd.read_csv(fileUrl)
symboldf['expiry'] = pd.to_datetime(symboldf['expiry']).apply(lambda x: x.date())   
symboldf


# In[ ]:


niftyDf = symboldf[(symboldf.instrument_type == 'OPTIDX') & (symboldf.tradingsymbol.str.startswith('BANKNIFTY')) &  (symboldf.exchange == 'NSE_FO')]
niftyDf


# In[ ]:


expiryList = niftyDf['expiry'].unique().tolist()
expiryList.sort()   
expiryList


# In[ ]:


expiryList[0]


# In[ ]:


symboldf[symboldf.tradingsymbol =='HDFC']


# In[ ]:


symboldf[(symboldf.instrument_type == 'FUTCOM') & (symboldf.tradingsymbol.str.startswith('SILVERMIC'))]


# In[ ]:


import requests

def make_request(method, url, headers=None, params=None, data=None):
    response = None

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=headers, params=params, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, params=params, json=data)
        else:
            raise ValueError('Invalid HTTP method.')

        
        if response.status_code == 200:
           
            return response.json()
        else:
            
            return response

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return None


# In[ ]:


url = 'https://api-v2.upstox.com/market-quote/quotes'
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Authorization': f'Bearer {access_token}'
}
params = {
    'symbol': 'NSE_EQ|INE848E01016,NSE_FO|43286'
}

response = make_request('GET', url, headers=headers, params=params)
response


# In[ ]:


url = 'https://api-v2.upstox.com/market-quote/ohlc'
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Authorization': f'Bearer {access_token}'
}
params = {
    'symbol': 'NSE_EQ|INE001A01036,NSE_FO|43286',
    'interval': 'I30'   
}

response = make_request('GET', url, headers=headers, params=params)
response


# In[ ]:


url = 'https://api-v2.upstox.com/market-quote/ltp'
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Authorization': f'Bearer {access_token}'
}
params = {
    'symbol': 'NSE_EQ|INE848E01016,NSE_EQ|INE001A01036'
}

response = make_request('GET', url, headers=headers, params=params)
response


# In[ ]:


instrument = urllib.parse.quote('MCX_FO|250060')
url = f'https://api-v2.upstox.com/historical-candle/{instrument}/1minute/2023-06-04/2023-06-01' 
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    
}

response = make_request('GET', url, headers=headers)
response


# In[ ]:


instrument = urllib.parse.quote('NSE_EQ|INE001A01036')
url = f'https://api-v2.upstox.com/historical-candle/intraday/{instrument}/1minute' 
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    
}

response = make_request('GET', url, headers=headers)
response


# In[ ]:




