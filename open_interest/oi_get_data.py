import os
os.system("pip install nsepy")
os.system("pip install datetime")
os.system("pip install pandas")
os.system("pip install numpy")
os.system("cls")
from nsepy import get_history
from datetime import date
import pandas as pd
import numpy as np

oiExists=os.path.exists("oi_data")
if(not oiExists):
    os.makedirs("oi_data")

# Demo List
company_list = ['ADANIENT','APOLLOHOSP','APOLLOTYRE','ASIANPAINT','AXISBANK','BAJFINANCE','BALKRISIND','AUROPHARMA',
     'BANKBARODA','BHARTIARTL','BEL','BPCL','BRITANNIA','CENTURYTEX','CANBK','CESC','COALINDIA','CIPLA',
     'COLPAL','CONCOR','DIVISLAB','DLF','GLENMARK','DRREDDY','EQUITAS','GODREJCP','EXIDEIND','HINDALCO',
     'FEDERALBNK','HINDPETRO','HAVELLS','HCLTECH','HDFC','ICICIBANK','IDFCFIRSTB','JSWSTEEL','INDIGO',
     'INFY','IOC','JUBLFOOD','JINDALSTEL','ADANIENT','RBLBANK','GMRINFRA','GRASIM','IGL']

no_comp = len(company_list)
print("Fetching data for {}".format(no_comp))
success_count = 0
fail_count = 0
i = 1
success_list = []
fail_list = []
for stock in company_list:
    try:
        print("\n"+str(i)+")")
        i += 1
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
        # OI_df['Close_Underlying']=data_vwap['Close']

        OI_df['Change_in_OI']=OI_df.OI_Combined.sub(OI_df.OI_Combined.shift(1))
        OI_df['Change_in_OI']=(OI_df['Change_in_OI'])/(OI_df['OI_Combined'])
        OI_df['Change_in_OI']=100*OI_df['Change_in_OI']

        OI_df['Change_in_VWAP']=OI_df.VWAP.sub(OI_df.VWAP.shift(1))
        OI_df['Change_in_VWAP']=(OI_df['Change_in_VWAP'])/(OI_df['VWAP'])
        OI_df['Change_in_VWAP']=100*OI_df['Change_in_VWAP']
        
        OI_df["PerDelivery"] = (OI_df["Delivery"]/OI_df["Volume"])*100

        OI_df.to_csv("oi_data/OI_combined_{}.csv".format(stock))
        print("Successfully fetched data for {}".format(stock))
        success_list.append(stock)
        success_count+=1
    except Exception as e:
        print("Failed to fetch data for {}".format(stock))
        print(str(e))
        fail_count += 1
        fail_list.append(stock)
    
    finally:
        print("Failed count = " + str(fail_count))
        print("Success count = " + str(success_count))

print("Successfully fetched data for {}".format(success_list))

print("Failed to fetch data for {}".format(fail_list))