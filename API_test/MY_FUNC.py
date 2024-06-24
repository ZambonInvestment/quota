import pandas as pd
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
from datetime import date, timedelta
import requests
import warnings


warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def fetch_data(tickers, start, end):
    data = pd.DataFrame()
    for ticker in tickers:
        try:
            df = yf.download(ticker, start=start, end=end)
            df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1, inplace=True)
            df.columns = [ticker]
            data = pd.concat([data, df], axis=1)
        except:
            pass
    return data

def get_ret(df,tickers):
  
  #____WEEKLY
  df1=(df.loc[(df.iloc[-1].name)-timedelta(days=7):])
  df1=df1.ffill()
  ret1= 100 * (1 + df1.pct_change()).cumprod()
  ret_w=round(ret1.iloc[-1]-100,2)
  #____MONTHLY
  df2=(df.loc[(df.iloc[-1].name)-timedelta(days=31):])
  df2=df2.ffill()
  ret2= 100 * (1 + df2.pct_change()).cumprod()
  ret_m=round(ret2.iloc[-1]-100,2)
  #____YEARLY
  df3=(df.loc[(df.iloc[-1].name)-timedelta(days=365):])
  df3=df3.ffill()
  ret3= 100 * (1 + df3.pct_change()).cumprod()
  ret_y=round(ret3.iloc[-1]-100,2)
  tab=pd.DataFrame({'Desc':[item[1] for item in tickers],
              'State':[item[2] for item in tickers],
              'Price':round(df.iloc[-1],2),
              'Δ% week':ret_w,
              'Δ% month':ret_m,
              'Δ% year':ret_y})
  time=str(df.iloc[-1].name)[:11]
  return ret_w,ret_m,ret_y,tab
