import pandas as pd
import os
import certifi

os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["SSL_CERT_FILE"] = certifi.where()
#url_for_raw_output = 'https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX.csv?limit=100&iss.only=analytics&iss.dp=comma&analytics.columns=tradedate,ticker,weight'
url_for_weight = 'https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX.csv?limit=100&iss.only=analytics&analytics.columns=ticker,shortnames,tradedate,weight' 
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
print(df_weight['weight'].sum())
#print(df_weight.describe())
print(df_marketsdata)

