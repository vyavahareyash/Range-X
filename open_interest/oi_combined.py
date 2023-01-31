import os
os.system("pip install nsepy")
os.system("pip install datetime")
os.system("pip install pandas")
os.system("pip install numpy")

from nsepy import get_history
from datetime import date
import pandas as pd
import numpy as np

stock='RELIANCE'
start=start=date(2022,12,1)
end=date(2023,1,25)
end2=date(2023,1,25)

data_fut = get_history(symbol=stock,futures=True,start=start, end=end, expiry_date=date(2022,12,29))
data_fut2 = get_history(symbol=stock,futures=True,start=start, end=end2, expiry_date=date(2023,1,25))

data_fut=data_fut.reset_index()
data_fut2=data_fut2.reset_index()

data_vwap=get_history(symbol=stock, start=date(2022,12,1), end=date(2023,1,25))
data_vwap=data_vwap.reset_index()

OI_df= pd.concat([data_fut2['Open Interest'],data_fut['Open Interest']],axis=1)

OI_df['OI_Combined']=OI_df.sum(axis=1)

OI_df['Date']=data_fut2['Date']
OI_df['Symbol']=data_fut2['Symbol']
OI_df['VWAP']=data_vwap['VWAP']
OI_df['Volume']=data_vwap['Volume']
OI_df['Delivery']=data_vwap['Deliverable Volume']
OI_df['Close_Underlying']=data_vwap['Close']

OI_df['Change_in_OI']=OI_df.OI_Combined.sub(OI_df.OI_Combined.shift(1))
OI_df['Change_in_OI']=(OI_df['Change_in_OI'])/(OI_df['OI_Combined'])
OI_df['Change_in_OI']=100*OI_df['Change_in_OI']

OI_df['Change_in_VWAP']=OI_df.VWAP.sub(OI_df.VWAP.shift(1))
OI_df['Change_in_VWAP']=(OI_df['Change_in_VWAP'])/(OI_df['VWAP'])
OI_df['Change_in_VWAP']=100*OI_df['Change_in_VWAP']

OI_df.to_csv("OI_combined.csv")
