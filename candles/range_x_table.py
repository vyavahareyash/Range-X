import os
import pandas as pd
from RangeX import table as t

# Check if tables folder already exists and create folder
tablesExists=os.path.exists("tables")
if(not tablesExists):
    os.makedirs("tables")

# Read the name of companies from data folder
fetchedDataList = os.listdir('data')
for i in range(len(fetchedDataList)):
    fetchedDataList[i]=fetchedDataList[i].split('.')[0]

# Test list
fetchedDataList = ['BAJAJFINSV_data', 'BHARTIARTL_data' ,'BRITANNIA_data' ,'KOTAKBANK_data', 'NATIONALUM_data', 'PFC_data', 'RELIANCE_data', 'WIPRO_data']

# Get start time as input
startTime=input('Enter start time [hh:mm] = ')
# Create folder for given start time
timeFolder=f'{startTime[:2]}_{startTime[3:]}'
timeExists=os.path.exists("tables/"+timeFolder)
if(not timeExists):
    os.makedirs("tables/"+timeFolder)

i=1


NPdata = pd.read_csv('NPvals.csv')
for company in fetchedDataList:    
    print(str(i)+")")
    i+=1
    n = NPdata[NPdata.isin([company.split('_')[0]])['Name']]['nMos'].astype('int8').values[0]
    p = NPdata[NPdata.isin([company.split('_')[0]])['Name']]['pMos'].astype('int8').values[0]
    t.get_table(company,startTime,timeFolder, pMos=p, nMos=n)

# os.system("cls")
print("Task completed")
