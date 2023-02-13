import os
from RangeX import table as t

tablesExists=os.path.exists("tables")
if(not tablesExists):
    os.makedirs("tables")

fetchedDataList = os.listdir('data')
for i in range(len(fetchedDataList)):
    fetchedDataList[i]=fetchedDataList[i].split('.')[0]

# fetchedDataList = ['RELIANCE_data']

startTime=input('Enter start time [hh:mm] = ')
timeFolder=f'{startTime[:2]}_{startTime[3:]}'
timeExists=os.path.exists("tables/"+timeFolder)
if(not timeExists):
    os.makedirs("tables/"+timeFolder)
i=1
for company in fetchedDataList:
    print(str(i)+")")
    i+=1
    t.get_table(company,startTime,timeFolder)

# os.system("cls")
print("Task completed")
