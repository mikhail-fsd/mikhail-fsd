import pandas as pd
import os
import certifi
import numpy as np
import sqlite3 

os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["SSL_CERT_FILE"] = certifi.where()
#url_for_raw_output = 'https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX.csv?limit=100&iss.only=analytics&iss.dp=comma&analytics.columns=tradedate,ticker,weight'

    
def update_data():

    url_for_weight = 'https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX.csv?limit=100&iss.only=analytics&analytics.columns=ticker,tradedate,weight' 
    url_for_lotsize_and_name = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.csv?iss.only=securities&securities.columns=SECID,SHORTNAME,LOTSIZE'

    df_weight = pd.read_csv(url_for_weight, sep=';', skiprows=2, index_col='ticker', parse_dates=['tradedate'], encoding='cp1251')
    df_lotsize_and_name = pd.read_csv(url_for_lotsize_and_name, sep=';', skiprows=2, index_col='SECID', encoding='cp1251')
    df = pd.concat([df_weight, df_lotsize_and_name], axis='columns', join='inner')
    #df = pd.concat([df_weight, df_lotsize_and_name, df_marketsdata], axis='columns', join='inner')
    df = df[['SHORTNAME', 'weight', 'tradedate', 'LOTSIZE']]
    df.columns = ['short_name', 'weight', 'weight_update', 'lot_size']
    df['tradedate'] = df['tradedate'].dt.strftime('%d.%m.%Y')

    con = sqlite3.connect('moex.db')

    df.to_sql('index_moex', con=con, if_exists='replace', index=True, index_label='ticker')


def get_price():

    url_for_marketdata = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.csv?iss.only=marketdata&marketdata.columns=SECID,LAST,UPDATETIME'
    df_marketsdata = pd.read_csv(url_for_marketdata, sep=';', skiprows=2, index_col='SECID', encoding='cp1251')
    df_marketsdata.columns = ['last_price', 'update_time']
    return df_marketsdata

def portfolio_init(start_budget, user_id=None): 

    con = sqlite3.connect('moex.db')
    df = pd.read_sql('select * from index_moex', con=con, index_col='ticker')
    df = pd.concat([df, get_price()], axis='columns', join='inner') # ['short_name', 'weight', 'weight_update', 'lot_size', 'last_price', 'update_time'],

    df['lot_cost'] = df['last_price'] * df['lot_size']
    
    df.sort_values(by='weight', ascending=False, inplace=True)
    df[['cash_to_spend', 'lots_to_buy']] = 0
    for row in df.index:
        df.at[row, 'lots_to_buy'] = round(start_budget * (df.loc[row, 'weight']/100) / df.loc[row, 'lot_cost'])
        df.at[row, 'cash_to_spend'] = df.loc[row, 'lots_to_buy'] * df.loc[row, 'lot_cost']
        if df['cash_to_spend'].sum() > start_budget:
            df.loc[row, ['lots_to_buy', 'cash_to_spend']] = 0
            break
    df.to_sql(f'goal_portfolio_{user_id}', con=con, if_exists='replace', index=True, index_label='ticker')
    rest_of_money = start_budget - df['cash_to_spend'].sum()
    portfolio_refill(rest_of_money, user_id, table_type='goal_')


def portfolio_refill(cash_refill, user_id, table_type='actual_'):
    con = sqlite3.connect('moex.db')
    user_table = f'{table_type}portfolio_{user_id}'
    sql = f"select * from {user_table}"
    df = pd.read_sql(sql=sql, con=con, index_col='ticker')
    
    df['my_weight'] = round((df['cash_to_spend'] / df['cash_to_spend'].sum()) * 100, 2)
    df['diff_weight'] = (df['weight'] - df['my_weight'])
    df.sort_values(by='diff_weight', ascending=False, inplace=True)
    df[['session_cash_to_spend', 'session_lots_to_buy']] = 0
    while cash_refill - df['session_cash_to_spend'].sum() >= df['lot_cost'].min():
        for row in df.index:
            if cash_refill - df['session_cash_to_spend'].sum() >= df.loc[row, 'lot_cost']:
                df.at[row, 'session_lots_to_buy'] += 1
                df.at[row, 'session_cash_to_spend'] += df.loc[row, 'lot_cost']
 
                df['my_weight'] = round(((df['cash_to_spend'] + df['session_cash_to_spend']) / (df['cash_to_spend'].sum() + df['session_cash_to_spend'].sum())) * 100, 2)
                df['diff_weight'] = (df['weight'] - df['my_weight'])
                df.sort_values(by='diff_weight', ascending=False, inplace=True)
                break 
 
    print(df['cash_to_spend'].sum(), df['session_cash_to_spend'].sum())
    df['cash_to_spend'] += df['session_cash_to_spend']
    df['lots_to_buy'] += df['session_lots_to_buy']

    print(df[['short_name', 'weight', 'lot_cost', 'lots_to_buy', 'cash_to_spend', 'my_weight', 'diff_weight']])
    print(df['cash_to_spend'].sum())
    df.to_sql(f'{user_table}', con=con, if_exists='replace', index=True, index_label='ticker')
    
def


def test():

    con = sqlite3.connect('moex.db')
    cur = con.cursor()
    res = cur.execute("select * from index_moex")
    #res = cur.execute("PRAGMA table_info('index_moex')")
    #print(res.fetchall())
    for row in res.fetchall():
        print(row)
portfolio_init(20_000, 11)
portfolio_refill(5_000, 11, table_type='goal_')
exit()
# нужна проверка на дату и сумму весов


#csv_weight = 'https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX.csv?limit=100&iss.dp=comma&analytics.columns=tradedate,ticker,weight'
#url = 'https://iss.moex.com/iss/statistics/engines/stock/markets/index/analytics/IMOEX.html?limit=100'
#df_IMOEX = pd.read_html(url, encoding='utf-8')[0]
#df_IMOEX.columns = [x.split()[0] for x in df_IMOEX.columns]
#df_IMOEX['tradedate'] = pd.to_datetime(df_IMOEX['tradedate'])
#df_IMOEX.to_csv('rer2.csv', encoding='cp1251', sep=';', date_format='%d.%m.%Y', decimal=',')

#df_weight = pd.read_csv('csv_weight')
#print(df_weight.describe())
#print(df_for_calc)
#print(df_for_calc['cash_to_spend3'].sum())
#print(df[['weight', 'lotcost', 'LOTSIZE', 'cash_to_spend', 'shares_to_buy', 'lots_to_buy', 'cash_to_spend2']])
#print(df['cash_to_spend'].sum())
#print(df['cash_to_spend2'].sum())

