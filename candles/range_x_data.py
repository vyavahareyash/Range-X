import os
from RangeX import data as d

# Check if data folder exists and create folder
dataExists=os.path.exists("data")
if(not dataExists):
    os.makedirs("data")

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

# Test list
company_list = ['RELIANCE']

# Initialize empty list to store the successfully fetched company names 
fetchedDataList=[]

# Fetch data in multiple rounds to retry for failed companies
round=1
while(round<=3): 
     print("Round "+str(round)+"\n")
     if round!=1:
          print("Retrying for "+str(failedList)+"\n")
     print(f"Fetching data for {len(company_list)} company(s)\n")
     successList, failedList = d.getData(company_list)
     fetchedDataList = fetchedDataList + successList
     if not len(failedList):
          break
     company_list=failedList
     round+=1

# os.system("cls")
print(f"{len(fetchedDataList)} data files fetched successfully\n")
print("Successfully fetched "+str(fetchedDataList)+"\n")
print("Failed to fetch "+str(failedList)+"\n")

# os.system("cls")
print("Task completed")
