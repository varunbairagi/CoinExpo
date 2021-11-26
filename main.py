from bs4 import BeautifulSoup 
import streamlit as slt
import requests
import pandas as pd
import json
import matplotlib.pyplot as plt

# page layout-->Divided in 2 col (col 1- price, col 2- graph)
col1, col2 = slt.columns((2,1)) 

# currency_price_unit = col1.selectbox('Select the unit of currency for price',('USD', 'BTC', 'ETH'))

# percent_timeframe = col1.selectbox('Percent change time frame',['7d','24h', '1h'])
# percent_dict = {"7d":'percentChange7d',"24h":'percentChange24h',"1h":'percentChange1h'}
# selected_percent_timeframe = percent_dict[percent_timeframe]

# sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

#web scraping from Coinmartketcap.com

@slt.cache
def load_data():
    my_Url = "https://coinmarketcap.com"
    r = requests.get(my_Url)
    html_content = r.content
    soup = BeautifulSoup(html_content, 'html.parser' )

    main_data = soup.find('script',id='_NEXT_DATA_',type='application/json')
    coins = {}
    coin_data = json.loads(main_data.contents[0])
    listing = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    for i in listing:
        coins[str(i['id'])] = i['slug']

    coin_name = []
    coin_symbol = []    
    market_cap = []
    percentage_change_1hr = []
    percentage_change_24hr = []
    percentage_change_7d = []
    price = []
    volume_24h = []

    for i in listing:
        coin_name.append(i['slug'])
        coin_symbol.append(i['symbol'])
        price.append(i['quote']['currency_price_unit']['price'])
        #percent_change_1hr percent_change_24hr percent_change_7d
        percentage_change_1hr.append(i['quote'][currency_price_unit]['percentChange1h']) 
        percentage_change_24hr.append(i['quote'][currency_price_unit]['percentChange24h']) 
        percentage_change_7d.append(i['quote'][currency_price_unit]['percentChange7d'])
        # market_cap 
        market_cap.append(i['quote'][currency_price_unit]['marketCap']) 
        # volume_24hr
        volume_24h.append(i['quote'][currency_price_unit]['volume24h']) 

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'marketCap', 'percentageChange1h', 'percentageChange24h', 'percentageChange7d', 'price', 'volume24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percentChange1h'] = percentage_change_1hr
    df['percentChange24h'] = percentage_change_24hr
    df['percentChange7d'] = percentage_change_7d
    df['marketCap'] = market_cap
    df['volume24h'] = volume_24h

    return df
df = load_data()

col1.dataframe(df)

col2.subheader('Table of % Price Change')
df_change = pd.concat([df.coin_symbol, df.percentChange1h, df.percentChange24h, df.percentChange7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percentChange1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percentChange24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percentChange7d'] > 0
col2.dataframe(df_change)

col2.subheader('Bar plot of % Price Change')

if percent_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percentChange7d'])
    col2.write('7 days period')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percentChange7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
    col2.pyplot(plt)
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percentChange24h'])
    col2.write('24 hour period')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percentChange24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
    col2.pyplot(plt)
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percentChange1h'])
    col2.write('1 hour period')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percentChange1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
    col2.pyplot(plt)