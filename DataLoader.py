import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

''' 
"stocks" dataframe contains daily historic YTD returns of 10 random stocks

'''

stocks = pd.read_excel("Data/grid1_pzafurjz.xlsx")
stocks.rename(columns= {'Unnamed: 0': "Date"},inplace = True)
stocks = stocks[stocks["Date"].isna() == False]


#data preprocessing

#### reverse order of dates
stocks = stocks[::-1]
stocks = stocks.reset_index()
stocks.drop("index", axis = 1, inplace = True)

#### removing US holidays
stocks = stocks[stocks["META US Equit"] != " "]

#### For Non US stocks, for Nan values copy the previous value
stocks.loc[stocks["RACE IM Equit"] == " ",
          ["IBE SM Equity","RACE IM Equit"]] = np.array(stocks.iloc[[66,81]][["IBE SM Equity","RACE IM Equit"]])

stocks = stocks.reset_index().drop("index", axis = 1)
stocks = stocks.set_index("Date")

#create return 
#could use this instead pd.pct_change
returns = stocks.astype(float)[1:].reset_index().sub(stocks.astype(float)[:-1].reset_index(), axis =1)
returns.drop("Date",inplace = True,axis =1)


returns = returns.div(stocks.astype(float)[:-1].reset_index().drop("Date",axis = 1)) *100


returns = stocks.pct_change()
#save data
stocks.to_csv('Data/ten_stocks.csv')
returns.to_csv('Data/ten_stocks_returns.csv')

#initialize indexes
sp100_companies = [
    'AAPL', 'ABBV', 'ABT', 'ACN', 'ADBE', 'AIG', 'ALL', 'AMGN', 'AMT', 'AMZN',
    'AXP', 'BA', 'BAC', 'BIIB', 'BK', 'BKNG', 'BLK', 'BMY', 'BRK-B', 'C', 'CAT',
    'CHTR', 'CL', 'CMCSA', 'COF', 'COP', 'COST', 'CRM', 'CSCO', 'CVS', 'CVX',
    'DD', 'DHR', 'DIS', 'DOW', 'DUK', 'EMR', 'EXC', 'F',  'FDX', 'GD',
    'GE', 'GILD', 'GM', 'GOOGL', 'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM',
    'KHC', 'KO', 'LIN', 'LLY', 'LMT', 'LOW', 'MA', 'MCD', 'MDLZ', 'MDT', 'MET', 'META',
    'MMM', 'MO', 'MRK', 'MS', 'MSFT', 'NEE', 'NFLX', 'NKE', 'NVDA', 'ORCL', 'PEP',
    'PFE', 'PG', 'PM', 'PYPL', 'QCOM', 'RTX', 'SBUX', 'SO', 'SPG', 'T', 'TGT',
    'TMO', 'TMUS', 'TSLA', 'TXN', 'UNH', 'UNP', 'UPS', 'USB', 'V', 'VZ', 'WBA',
    'WFC', 'WMT', 'XOM'
]



import yfinance as yf
# Define the start and end dates
start_date = '2018-01-01'
end_date = '2023-06-07'

# Create an empty DataFrame to store the data
sp100_data = pd.DataFrame()

# Retrieve data for each ticker symbol
for symbol in sp100_companies:
    try:
        # Download historical data using yfinance
        data = yf.download(symbol, start=start_date, end=end_date)
        
        # Extract the 'Open' column and add it to sp100_data DataFrame
        sp100_data[symbol] = data['Open']
    except Exception as e:
        print(f"Error retrieving data for {symbol}: {e}")

# Remove Nan columns
nan_bool_df = sp100_data.isna()  
columns_with_nan = nan_bool_df.any()
sp100_data.drop(sp100_data.columns[columns_with_nan][0],inplace = True,axis=1)

sp100returns = sp100_data.pct_change()

sp100returns.to_csv('Data/sp100returns.csv')
sp100_data.to_csv('Data/sp100_data.csv')


#creation market cap dataframe for value weighted portfolio

market_cap = pd.DataFrame()

for symbol in sp100_companies:
    try:
        market_cap[symbol] = sp100_data[symbol] * yf.Ticker(symbol).info['sharesOutstanding']
    except:
        market_cap[symbol] = sp100_data[symbol] * (yf.Ticker(symbol).info['marketCap'] / yf.Ticker(symbol).info['open'])
        

# Remove Nan columns
nan_bool_df = market_cap.isna()  
columns_with_nan = nan_bool_df.any()
sp100_data.drop(market_cap.columns[columns_with_nan][0],inplace = True,axis=1)

#save data


market_cap.to_csv('Data/market_cap.csv')