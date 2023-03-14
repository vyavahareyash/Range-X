import os
from RangeX import table as t

tablesExists=os.path.exists("tables")
if(not tablesExists):
    os.makedirs("tables")

fetchedDataList = os.listdir('data')
for i in range(len(fetchedDataList)):
    fetchedDataList[i]=fetchedDataList[i].split('.')[0]

fetchedDataList = ['BAJAJFINSV_data', 'BHARTIARTL_data' ,'BRITANNIA_data' ,'KOTAKBANK_data', 'NATIONALUM_data', 'PFC_data', 'RELIANCE_data', 'WIPRO_data']

startTime=input('Enter start time [hh:mm] = ')
timeFolder=f'{startTime[:2]}_{startTime[3:]}'
timeExists=os.path.exists("tables/"+timeFolder)
if(not timeExists):
    os.makedirs("tables/"+timeFolder)
i=1
for company in fetchedDataList:
    print(str(i)+")")
    i+=1
    t.get_table(company,startTime,timeFolder,
                pMos=int(input(f'Enter pMos for {company}')),
                nMos=int(input(f'Enter nMos for {company}')))

# os.system("cls")
print("Task completed")
