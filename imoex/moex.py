import pandas as pd
import os
import certifi
import numpy as np
import sqlite3 

os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["SSL_CERT_FILE"] = certifi.where()
#url_for_raw_output = 'https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX.csv?limit=100&iss.only=analytics&iss.dp=comma&analytics.columns=tradedate,ticker,weight'

    
url_for_weight = 'https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX.csv?limit=100&iss.only=analytics&analytics.columns=ticker,tradedate,weight' 
url_for_lotsize_and_name = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.csv?iss.only=securities&securities.columns=SECID,SECNAME,SHORTNAME,LOTSIZE'
url_for_marketdata = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.csv?iss.only=marketdata&marketdata.columns=SECID,LAST,UPDATETIME,TIME'

df_weight = pd.read_csv(url_for_weight, sep=';', skiprows=2, index_col='ticker', parse_dates=['tradedate'], encoding='cp1251')
df_lotsize_and_name = pd.read_csv(url_for_lotsize_and_name, sep=';', skiprows=2, index_col='SECID', encoding='cp1251')
df_marketsdata = pd.read_csv(url_for_marketdata, sep=';', skiprows=2, index_col='SECID', encoding='cp1251')


# нужна проверка на дату и сумму весов


#csv_weight = 'https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX.csv?limit=100&iss.dp=comma&analytics.columns=tradedate,ticker,weight'
#url = 'https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX.html?limit=100'
#df_IMOEX = pd.read_html(url, encoding='utf-8')[0]
#df_IMOEX.columns = [x.split()[0] for x in df_IMOEX.columns]
#df_IMOEX['tradedate'] = pd.to_datetime(df_IMOEX['tradedate'])
#df_IMOEX.to_csv('rer2.csv', encoding='cp1251', sep=';', date_format='%d.%m.%Y', decimal=',')

#df_weight = pd.read_csv('csv_weight')
#print(df_weight.describe())
budget = 100_000
df = pd.concat([df_weight, df_lotsize_and_name, df_marketsdata], axis='columns', join='inner')
df['lotcost'] = df['LAST'] * df['LOTSIZE']
df['cash_to_spend'] = budget * (df['weight']/100) 
df['shares_to_buy'] = budget * (df['weight']/100) // df['LAST']
df['lots_to_buy'] = round(budget * (df['weight']/100) / df['lotcost'])
df['cash_to_spend2'] = df['lots_to_buy'] * df['lotcost']

df_for_calc = df[['weight', 'lotcost']].sort_values(by='weight', ascending=False)
df_for_calc['cash_to_spend3'] = np.zeros((40,1))
print(df_for_calc)
for x in range(df.shape[0]):
    df_for_calc.iat[x, 2] = round(budget * (df_for_calc.iloc[x]['weight']/100) / df_for_calc.iloc[x]['lotcost']) * df_for_calc.iloc[x]['lotcost']
    if df_for_calc['cash_to_spend3'].sum() > budget:
        break
print(df_for_calc)
print(df_for_calc['cash_to_spend3'].sum())
#print(df[['weight', 'lotcost', 'LOTSIZE', 'cash_to_spend', 'shares_to_buy', 'lots_to_buy', 'cash_to_spend2']])
#print(df['cash_to_spend'].sum())
#print(df['cash_to_spend2'].sum())

