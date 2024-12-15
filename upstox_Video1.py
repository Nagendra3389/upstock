#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import urllib.parse
import pandas as pd
import requests


# In[ ]:


apiKey = ''
secretKey = ''
redirectUrl = ''
rurl = urllib.parse.quote(redirectUrl,safe="")
rurl


# In[ ]:


uri = f'https://api-v2.upstox.com/login/authorization/dialog?response_type=code&client_id={apiKey}&redirect_uri={rurl}'
uri


# In[ ]:





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


niftyDf[niftyDf.expiry == expiryList[0]]

