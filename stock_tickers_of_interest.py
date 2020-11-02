import pandas as pd
import datapane as dp
from datetime import datetime, timedelta
# ['symbol', 'name', 'price', 'priceChange', 'percentChange',
#  'exchangeName', 'exShortName', 'exchangeCode', 'marketPlace', 'sector',
#  'industry', 'volume', 'openPrice', 'dayHigh', 'dayLow', 'MarketCap',
#  'MarketCapAllClasses', 'peRatio', 'prevClose', 'dividendFrequency',
#  'dividendYield', 'dividendAmount', 'dividendCurrency', 'beta', 'eps',
#  'exDividendDate', 'shortDescription', 'longDescription', 'website',
#  'email', 'phoneNumber', 'fullAddress', 'employees', 'shareOutStanding',
#  'totalDebtToEquity', 'totalSharesOutStanding', 'sharesESCROW', 'vwap',
#  'dividendPayDate', 'weeks52high', 'weeks52low', 'alpha',
#  'averageVolume10D', 'averageVolume30D', 'averageVolume50D',
#  'priceToBook', 'priceToCashFlow', 'returnOnEquity', 'returnOnAssets',
#  'day21MovingAvg', 'day50MovingAvg', 'day200MovingAvg', 'dividend3Years',
#  'dividend5Years', 'datatype', '__typename']

url = 'https://raw.githubusercontent.com/FriendlyUser/cad_tickers_list/main/static/latest/stocks.csv'
stock_df = pd.read_csv(url, error_bad_lines=False)
# Remove duplicates by table
stock_df = stock_df[
    [
        "symbol",
        "price",
        "volume",
        "sector",
        "industry",
        "peRatio",
        "shortDescription",
    ]
]

industries = [
    "Restaurants",
    "Asset Management",
    "Forest Products",
    "Oil & Gas",
    "Industrial Products",
    "Biotechnology",
    "Farm & Heavy Construction Machinery",
    "Business Services",
    "Chemicals",
    "Medical Diagnostics & Research",
    "Metals & Mining",
    "Utilities - Independent Power Producers",
    "Retail - Defensive",
    "Utilities - Regulated",
    "REITs",
    "Banks",
    "Drug Manufacturers",
    "Aerospace & Defense",
    "Other Energy Sources",
    "Construction",
    "Hardware",
    "Real Estate",
    "Beverages - Alcoholic",
    "Retail - Cyclical",
    "Personal Services",
    "Building Materials",
    "Conglomerates",
    "Vehicles & Parts",
    "Capital Markets",
    "Manufacturing - Apparel & Accessories",
    "Travel & Leisure",
    "Healthcare Providers & Services",
    "Software",
    "Transportation",
    "Education",
    "Telecommunication Services",
    "Credit Services",
    "Consumer Packaged Goods",
    "Insurance",
    "Interactive Media",
    "Media - Diversified",
    "Industrial Distribution",
    "Agriculture",
    "Beverages - Non-Alcoholic",
    "Medical Devices & Instruments",
    "Diversified Financial Services",
    "Furnishings, Fixtures & Appliances",
    "Steel",
    "Packaging & Containers",
    "Semiconductors",
    "Waste Management",
    "Healthcare Plans",
]

def industry_to_md(industry_list):
  return '\n'.join([f'* {i}' for i in industry_list])

pattern = '(?i)Waste Management|(?i)Interactive Media|(?i)Telecommunication Services|(?i)Software|(?i)Hardware'

desired_df = stock_df[stock_df['industry'].str.contains(pattern, na=False)]

industry_list = industry_to_md(industries)
curr_date = datetime.today().strftime('%Y-%m-%d')
r = dp.Report(
    f'### Desired Stocks for {curr_date}',
    dp.Table(desired_df),
    f'### Industry List',
    f'{industry_list}'
    )
r.save(path='industry_index.html')

r.publish(name='Desired Tickers',  open=False, tweet=False)
