import pandas as pd
import datapane as dp
import yfinance as yf
import matplotlib.pyplot as plt
import random
import os
from datetime import datetime, timedelta
def generate_up(stocks: list, start_date: str="2020-03-01", end_date: str="2020-05-30"):
    stocks_string = " ".join(stocks)
    data = yf.download(stocks_string, start=start_date, end=end_date,
                      group_by="ticker")
    data = data.fillna(method='ffill')
    # Drop columns with no entries
    data = data.dropna(axis='columns', how='all')

    full_df = pd.concat([data[ticker]["Close"] for ticker in stocks], axis=1)
    full_df.columns = stocks
    full_df = full_df.sort_index(ascending=False)
    return full_df

def random_line_color():
    return random.choice([
        'black',
        'blue',
        'red',
        'green'
    ])

def intraday_plot(stock_ticker: str, start_date: str="2020-03-01", end_date: str="2020-05-30"):
    plt.figure(figsize=(8, 8))
    data = yf.download(stock_ticker, start=start_date, end=end_date, interval='30m')
    random_color = random_line_color()
    ax = data['Close'].plot(color=random_color)
    ax.set_xlabel("Date")
    # Eventually map .CN, .V to CAD
    # only cad stocks for now
    ax.set_ylabel("Price ($)")
    ax.set_title(f"{stock_ticker} - {start_date} to {end_date}")
    # ax.set_color(random_color)
    return ax


stock_list = ["NTAR.CN",
    "IDK.CN", 
    "ART.V",
    "PKK.CN",
    "APHA.TO",
    "CMC.CN",
    "AMPD.CN",
    "MTRX.V"]

curr_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=59)).strftime('%Y-%m-%d')

df_assets = generate_up(stock_list, start_date, curr_date)

figure_list = [dp.Plot(intraday_plot(stock, start_date, curr_date)) for stock in stock_list]


publish_report = False
dp_token = os.getenv('DP_TOKEN')
if dp_token:
    # login
    try:
        publish_report = True
    except Exception as e:
        print(e)

# login
r = dp.Report(
    f'### Intraday Report for {curr_date}',
    dp.Table(df_assets), 
    dp.Blocks(*figure_list, columns=2))
r.save(path='index.html', open=True)

if publish_report == True:
    r.publish(name='Daily Report',  open=False, tweet=False)
