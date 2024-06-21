
import pandas as pd
import matplotlib.pyplot as plt
import io
from PIL import Image
import telegram
import pandas as pd
import numpy as np
import yfinance as yf
import pandas_datareader.data as web
import datetime
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import dataframe_image as dfi
from datetime import date, timedelta
import requests
import warnings
import seaborn
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




def correlation_dt(df,days):
        returns_pl=(df.loc[(df.iloc[-1].name)-timedelta(days=days):]).pct_change().dropna()
        corr_df=returns_pl.corr(method='pearson')
        time=str(df.iloc[-1].name)[:11]
        plt.close() 
        plt.figure(figsize=(10,6))
        mask = np.zeros_like(corr_df)
        mask[np.triu_indices_from(mask)] = True
        #generate plot
        ax=seaborn.heatmap(corr_df, cmap='RdYlGn', vmax=1.0, vmin=-1.0 , mask = mask, linewidths=2.5,annot=True)
           
        cbar = ax.collections[0].colorbar
        # here set the labelsize by 20
        cbar.ax.tick_params(labelsize=12)
        ttx=str(df.iloc[-1].name)[:11]
        plt.title('1y Correlation of returns on')
        plt.yticks(rotation=0,fontsize=12) 
        plt.xticks(rotation=0,fontsize=12)
        plt.show()
        plt.savefig('Exch_Corr_'+time+'.png')
        #plt.close()
        
        return plt

def show_index(df,ticker,basemap,days):
    ret_w,ret_m_,ret_y,tab=get_ret(df,ticker)
    time=str(df.iloc[-1].name)[:11]
    plt.rcParams["figure.figsize"] = (50,25)
    m=basemap
    m.drawcoastlines()
    m.fillcontinents(color='grey',lake_color='white')
      # draw parallels and meridians.
    m.drawparallels(np.arange(-90.,120.,30.))
    m.drawmeridians(np.arange(0.,420.,60.))
    m.drawmapboundary(fill_color='white')
      #_______________________________________
    plt.title(f'Exchanges @ {time}')
    tab.dfi.export('Exch_Stat_'+time+'.png',fontsize=22)
    
    for i in np.arange(len(ticker)):
        lon,lat= (ticker[i][3]),(ticker[i][4])
        xpt,ypt = m(lon,lat)
        lonpt, latpt = m(xpt,ypt,inverse=True)
        #_____POSTIVE GREEN - NEGATIVE RED
        if ret_w[i]>0:
          col='green'
        else:
          col='red'
            
        txt=ticker[i][0]+'| Δ week:'+str(ret_w[i])+'%'
    #+'% | M:'+str(ret_m[i])+'% | Y:'+str(ret_y[i])+'%'
        plt.text(xpt,ypt,txt, #% (stock_exch[i][0])
                                fontsize=42,
                                bbox=dict(boxstyle="round",
                                color=col,
                                edgecolor='black',
                              ))
                              
    plt.savefig('Exch_Fig_'+time+'.png')
    plt.close()
    
    
    return (tab, plt.show())


