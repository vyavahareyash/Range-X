import os
# os.system("pip install nsepy")
# os.system("pip install datetime")
# os.system("pip install pandas")
# os.system("cls")

from nsepy import get_history
from datetime import date
import pandas as pd

destination_folder = "oi_data_JAN_FEB"

oiExists=os.path.exists(destination_folder)
if(not oiExists):
    os.makedirs(destination_folder)


company_list = ['ADANIENT','APOLLOHOSP','APOLLOTYRE','ASIANPAINT','AXISBANK','BAJFINANCE','BALKRISIND','AUROPHARMA',
     'BANKBARODA','BHARTIARTL','BEL','BPCL','BRITANNIA','CENTURYTEX','CANBK','CESC','COALINDIA','CIPLA',
     'COLPAL','CONCOR','DIVISLAB','DLF','GLENMARK','DRREDDY','EQUITAS','GODREJCP','EXIDEIND','HINDALCO',
     'FEDERALBNK','HINDPETRO','HAVELLS','HCLTECH','HDFC','ICICIBANK','IDFCFIRSTB','JSWSTEEL','INDIGO',
     'INFY','IOC','JUBLFOOD','JINDALSTEL','KOTAKBANK','LUPIN','MARICO','L&TFH','LICHSGFIN','LT','MARUTI',
     'MCDOWELL-N','MOTHERSUMI','MRF','NATIONALUM','NESTLEIND','NIITTECH','NMDC','NTPC','PAGEIND','OIL','PFC',
     'PNB','POWERGRID','ONGC','PVR','ACC','RECLTD','RELIANCE','SBIN','SUNPHARMA','TATACONSUM','TATAPOWER','TECHM',
     'TORNTPHARM','SRTRANSFIN','UJJIVAN','UPL','WIPRO','ADANIPOWER','ASHOKLEY','BATAINDIA','BERGEPAINT','TATASTEEL',
     'CHOLAFIN','CUMMINSIND','DABUR','TCS','EICHERMOT','ESCORTS','GAIL','HEROMOTOCO','INDUSINDBK','ITC','M&M','BIOCON',
     'MANAPPURAM','MFSL','MGL','MINDTREE','NCC','PEL','RAMCOCEM','SAIL','TATAMOTORS','TORNTPOWER','TVSMOTOR',
     'ADANIPORTS','VEDL','VOLTAS','BAJAJ-AUTO','BAJAJFINSV','BHARATFORG','HINDUNILVR','IBULHSGFIN','ICICIPRULI','BHEL',
     'INFRATEL','PIDILITIND','SIEMENS','SRF','SUNTV','TITAN','ULTRACEMCO','HDFCBANK','JUSTDIAL','PETRONET','ZEEL','CADILAHC',
     'TATACHEM','AMBUJACEM','RBLBANK','GMRINFRA','GRASIM','IGL','MUTHOOTFIN','UBL','IDEA','AMARAJABAT','YESBANK','BANDHANBNK',
     'HDFCLIFE','NAUKRI']

# Demo List
# company_list = ['PVR']

n_comp = len(company_list)
print(f"Fetching data for {n_comp}")
success_count = 0
fail_count = 0
i = 1
success_list = []
fail_list = []
for stock in company_list:
    try:
        print("\n"+str(i)+")")
        i += 1
        
        start=start=date(2023,1,1)
        end=date(2023,2,23)
        end2=date(2023,2,23)
        # start=start=date(2022,12,1)
        # end=date(2023,1,25)
        # end2=date(2023,1,25)
        
        data_fut = get_history(symbol=stock,futures=True,start=start, end=end, expiry_date=date(2023,1,25))
        data_fut2 = get_history(symbol=stock,futures=True,start=start, end=end2, expiry_date=date(2023,2,23))
        # data_fut = get_history(symbol=stock,futures=True,start=start, end=end, expiry_date=date(2022,12,29))
        # data_fut2 = get_history(symbol=stock,futures=True,start=start, end=end2, expiry_date=date(2023,1,25))

        data_fut=data_fut.reset_index()
        data_fut2=data_fut2.reset_index()

        # data_vwap=get_history(symbol=stock, start=date(2022,12,1), end=date(2023,1,25))
        data_vwap=get_history(symbol=stock, start=date(2023,1,1), end=date(2023,2,23))
        
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

        OI_df.to_csv(f"{destination_folder}/{stock}_OI_combined.csv")
        print(f"Successfully fetched data for {stock}")
        success_list.append(stock)
        success_count+=1
        
    except Exception as e:
        print(f"Failed to fetch data for {stock}")
        print(str(e))
        fail_count += 1
        fail_list.append(stock)
    
    finally:
        print("Failed count = " + str(fail_count))
        print("Success count = " + str(success_count))

print("Successfully fetched data for {}".format(success_list))

if len(fail_list):
    print("Failed to fetch data for {}".format(fail_list))