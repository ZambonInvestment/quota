from DATASET_SETTING import *
from PERIMETER import *
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
import telegram
#df_EU=fetch_data(EU_tick,
#          '2021-06-02',
 #          '2024-06-14')
#df_AM=fetch_data(AM_tick,
 #          '2021-06-02',
#           '2024-06-14')
#df_AS=fetch_data(AM_tick,
#           '2021-06-02',
#         '2024-06-14')

EU_tick = [item[0] for item in EU]
AM_tick = [item[0] for item in US]
AS_tick = [item[0] for item in ASIA]

Basemap_EU=Basemap(projection='merc', llcrnrlat=34, urcrnrlat=60, llcrnrlon=-15, urcrnrlon=40, resolution='l')
Basemap_AM=Basemap(projection='merc', llcrnrlat=-60, urcrnrlat=70, llcrnrlon=-150, urcrnrlon=-30, resolution='l')
Basemap_AS=Basemap(projection='merc', llcrnrlat=-60, urcrnrlat=70, llcrnrlon=30, urcrnrlon=170, resolution='l')

days=365
show_index(fetch_data(EU_tick,'2022-06-02','2024-06-14'),EU,Basemap_EU,365)
correlation_dt(fetch_data(EU_tick,'2022-06-02','2024-06-14'),days)


show_index(fetch_data(AS_tick,'2022-06-02','2024-06-14'),ASIA,Basemap_AS,365)
correlation_dt(fetch_data(AS_tick,'2022-06-02','2024-06-14'),days)


show_index(fetch_data(AM_tick,'2022-06-02','2024-06-14'),US,Basemap_AM,365)
correlation_dt(fetch_data(AM_tick,'2022-06-02','2024-06-14'),days)
