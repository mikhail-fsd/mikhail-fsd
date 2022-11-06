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
    df['weight_update'] = df['weight_update'].dt.strftime('%d.%m.%Y')

    con = sqlite3.connect('moex.db')

    df.to_sql('index_moex', con=con, if_exists='replace', index=True, index_label='ticker')

def get_data_dframe():

    con = sqlite3.connect('moex.db')
    df = pd.read_sql('select * from index_moex', con=con, index_col='ticker')
    return df

def update_price():

    url_for_marketdata = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.csv?iss.only=marketdata&marketdata.columns=SECID,LAST,UPDATETIME'
    df = pd.read_csv(url_for_marketdata, sep=';', skiprows=2, index_col='SECID', encoding='cp1251')
    df.columns = ['last_price', 'price_update_time']

    con = sqlite3.connect('moex.db')

    df.to_sql('price_moex', con=con, if_exists='replace', index=True, index_label='ticker')

def get_price_dframe():
    con = sqlite3.connect('moex.db')
    df = pd.read_sql('select * from price_moex', con=con, index_col='ticker')
    df_lot_size = pd.read_sql('select ticker, lot_size from index_moex', con=con, index_col='ticker')
    df = pd.concat([df, df_lot_size], axis='columns', join='inner')
    df['lot_cost'] = df['last_price'] * df['lot_size']
    df.drop(columns=['lot_size'], inplace=True)
    return df
   
def get_user_pirtfolio_dframe(user_id):
    con = sqlite3.connect('moex.db')
    user_table = f'portfolio_{user_id}'
    sql = f'select * from {user_table}'
    df = pd.read_sql(sql=sql, con=con, index_col='ticker')
    return df
    

def user_init(user_id, name, goal=0, phone=''):
    
    con = sqlite3.connect('moex.db')
    cur = con.cursor()
    cur.execute("""create table if not exists users_table(
                user_id INTEGER PROMARY KEY,
                user_name TEXT,
                user_goal INTEGER,
                phone TEXT
                )""")
    cur.execute("insert into users_table values (:user_id, :user_name, :user_goal, :phone)", {'user_id':user_id, 'user_name':name, 'user_goal':goal, 'phone':phone})
    con.commit()







def portfolio_init(start_budget, base_df=None): # rough calc
    """ если на вход не подается базовая таблица, то за базу берется таблица из DB index_moex
    
    """
    if base_df is None:
        base_df = get_data_dframe()
        df = pd.concat([base_df, get_price_dframe()], axis='columns', join='inner') # ['short_name', 'weight', 'weight_update', 'lot_size', 'last_price', 'update_time'],
    else:
        df = base_df
    
    df.sort_values(by='weight', ascending=False, inplace=True)
    df[['total_shares_price', 'lots_to_buy']] = 0
    for row in df.index:
        df.at[row, 'lots_to_buy'] = round(start_budget * (df.loc[row, 'weight']/100) / df.loc[row, 'lot_cost'])
        df.at[row, 'total_shares_price'] = df.loc[row, 'lots_to_buy'] * df.loc[row, 'lot_cost']
        if df['total_shares_price'].sum() > start_budget:
            df.loc[row, ['lots_to_buy', 'total_shares_price']] = 0
            break
    #df.to_sql(f'goal_portfolio', con=con, if_exists='replace', index=True, index_label='ticker')
    rest_of_money = start_budget - df['total_shares_price'].sum()
    df = portfolio_refill(rest_of_money, df=df)
    return df


def user_porfolio_init(user_id):
    con = sqlite3.connect('moex.db')
    df = pd.read_sql('select ticker from index_moex', con=con, index_col='ticker')
    df[['my_shares', 'my_lots']] = 0
    table_name = f'portfolio_{user_id}'
    df.to_sql(table_name, con=con, if_exists='replace', index=True, index_label='ticker')

def portfolio_refill(cash_refill, df, user_id=''):  # tight count
   # con = sqlite3.connect('moex.db')
   # if user_id: user_id = '_' + str(user_id)
   # user_table = f'{table_type}portfolio{user_id}'
   # sql = f"select * from {user_table}"
   # df = pd.read_sql(sql=sql, con=con, index_col='ticker')
    if user_id:
        df_price = get_price_dframe()
        df_data = get_data_dframe()
        df = pd.concat([df, df_price, df_data['weight']], axis='columns', join='inner')
        df['total_shares_price'] = df['my_lots'] * df['lot_cost']

        df['lots_to_buy'] = 0  # для юзеров не используется, используется при расчете goals_portfolio

    df['my_weight'] = round((df['total_shares_price'] / df['total_shares_price'].sum()) * 100, 2).fillna(0)
    df['diff_weight'] = (df['weight'] - df['my_weight'])
    df.sort_values(by='diff_weight', ascending=False, inplace=True)
    df[['session_cash_to_spend', 'session_lots_to_buy']] = 0
    while cash_refill - df['session_cash_to_spend'].sum() >= df.loc[df['diff_weight'] > 0]['lot_cost'].min():
        for row in df.index:
            if cash_refill - df['session_cash_to_spend'].sum() >= df.loc[row, 'lot_cost']:
                df.at[row, 'session_lots_to_buy'] += 1
                df.at[row, 'session_cash_to_spend'] += df.loc[row, 'lot_cost']
 
                df['my_weight'] = round(((df['total_shares_price'] + df['session_cash_to_spend']) / (df['total_shares_price'].sum() + df['session_cash_to_spend'].sum())) * 100, 2)
                df['diff_weight'] = (df['weight'] - df['my_weight'])
                df.sort_values(by='diff_weight', ascending=False, inplace=True)
                break 
 
    #print(df['total_shares_price'].sum(), df['session_cash_to_spend'].sum())
    df['total_shares_price'] += df['session_cash_to_spend']
    df['lots_to_buy'] += df['session_lots_to_buy']


    #print(df[['short_name', 'weight', 'lot_cost', 'lots_to_buy', 'total_shares_price', 'my_weight', 'diff_weight']])
    #print(df['total_shares_price'].sum())

    return df

    #df.to_sql(f'{user_table}', con=con, if_exists='replace', index=True, index_label='ticker')
    
def goals_portfolio_init():
     
    df = None

    lst = np.concatenate([np.arange(50_000, 250_000, 50_000), np.arange(300_000, 1_100_000, 100_000)])
    for goal_budget in lst:
        if df is None: df = portfolio_init(goal_budget) # когда таблица рассчитывается первый раз, то базовая таблица будет таблицей из DB index_moex 
        column_lot_name = f'goal_lots_amount_for_{goal_budget}'
        column_sum_name = f'goal_sum_for_{goal_budget}'
        column_weight_name = f'weight_when_buy_on_{goal_budget}'
        df_temp = portfolio_init(goal_budget)# base_df=df) 
        df[[column_lot_name, column_sum_name, column_weight_name]] = df_temp[['lots_to_buy', 'total_shares_price', 'my_weight']]
    columns_list = [x for x in df.columns if x.startswith('goal')]
    df = df[columns_list]
    con = sqlite3.connect('moex.db')
    df.to_sql('goal_portfolio', con=con, if_exists='replace', index=True, index_label='ticker')



def get_buy_offer(user_id, cash_to_spend):
    df_user_portfolio = get_user_pirtfolio_dframe(user_id)
    df_offer = portfolio_refill(cash_to_spend, user_id=user_id, df=df_user_portfolio)
    return df_offer


def buy_securities(user_id, ticker_name, value, lot_or_share):

    ticker_name = f'\'{ticker_name}\''
    
    con = sqlite3.connect('moex.db')
    cur = con.cursor()

    lot_size = cur.execute(f"SELECT lot_size FROM index_moex WHERE ticker = {ticker_name}").fetchone()[0]

    if lot_or_share == 'share':
        shares = value
        lots = value / lot_size
    elif lot_or_share == 'lot':
        shares = value * lot_size
        lots = value

    user_table = f'portfolio_{user_id}'
    cur.execute(f"UPDATE {user_table} SET my_shares = my_shares + {shares}, my_lots = my_lots + {lots} WHERE ticker = {ticker_name}")
    con.commit()

def securities_sell():
    pass


#user_porfolio_init(3233)
#print(get_buy_offer(3233, 10_000)['diff_weight'])
#budget = 40_000
#df1 = portfolio_init(budget)[['lots_to_buy', 'total_shares_price']]
#df2 = get_buy_offer(3233, budget)[['session_lots_to_buy', 'session_cash_to_spend']] 
#df3 = pd.concat([df1, df2], axis='columns', join='inner')
#file ='/mnt/c/Users/Mikhail/OneDrive/backup/res.csv' 
#update_data()
#update_price()
#file = ''
#goals_portfolio_init()
#df3.to_csv(file, sep=';', encoding='cp1251', decimal=',')


def test():

    con = sqlite3.connect('moex.db')
    cur = con.cursor()
    #cur.execute('update portfolio_3233 set my_shares = 0, my_lots = 0 where ticker = "AFLT"') 
    res = cur.execute('select * from portfolio_3233')
    #res = cur.execute("select * from index_moex")
    #res = cur.execute("PRAGMA table_info('index_moex')")
    #res = cur.execute("select name from sqlite_master where type = 'table'")
    #print(res.fetchall())
    con.commit()
    print(res.fetchone())
    for row in res.fetchall():
        print(row)
buy_securities(3233, 'GAZP', 1, 'lot')
#user_porfolio_init(3233)
df2 = get_buy_offer(3233, 10_000)[['session_lots_to_buy', 'session_cash_to_spend']] 
print(df2)
test()



