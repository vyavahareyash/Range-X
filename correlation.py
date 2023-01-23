import numpy as np 
import pandas as pd
import os

corrExists=os.path.exists("correlations")
if(not corrExists):
    os.makedirs("correlations")

timeList = os.listdir('tables')

for time in timeList:
    corrTable = pd.DataFrame()
    companyList = os.listdir('tables/'+time)
    corrTable['company']=np.array(companyList)
    corrList=[]
    for company in companyList:
        data = pd.read_csv('tables/{}/{}'.format(time,company))
        size = data['Candle_size']
        reversal = data['tReversal']
        corrList.append(size.corr(reversal))
    corrTable['correlation']=np.array(corrList)
    corrTable.to_csv('correlations/{}_corr.csv'.format(time),index=False)
        
        
