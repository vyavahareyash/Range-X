import numpy as np
import pandas as pd
import os
from RangeX import table as t

#Demo List
company_list = ['BAJAJFINSV', 'BHARTIARTL' ,'BRITANNIA' ,'KOTAKBANK', 'NATIONALUM', 'PFC', 'RELIANCE', 'WIPRO']

# startTime='10:15'
startTime=input('Enter start time [hh:mm] = ')
i = 0
for company in company_list :
    pMosList = nMosList = np.arange(5)
    plist=[]
    nlist=[]
    clist=[]
    outList=[]
    df = pd.DataFrame(columns=['pMos','nMos','total_reversals','total_margin','outlier %'])
    for pMos in pMosList:
        for nMos in nMosList:
            # count, totalDays = get_table_count(company,startTime,pMos,nMos)
            count, totalDays = t.get_table(company+'_data',startTime,pMos,nMos,save=False)
            plist.append(pMos)
            nlist.append(nMos)
            clist.append(count)
            outper = '{:.2f}'.format((count/totalDays)*100)
            outList.append(outper)
    df['pMos']=np.array(plist)
    df['nMos']=np.array(nlist)
    df['total_reversals']=np.array(clist)
    df['outlier %']=np.array(outList)

    df['total_margin']=abs(df['pMos']+df['nMos'])
    df.sort_values(by='total_reversals',inplace=True,ascending=True)
    df.reset_index(inplace=True,drop=True)
    df = df.loc[df.groupby('total_reversals').total_margin.idxmin()].reset_index(drop=True)
    df = df.loc[df.groupby('total_margin').total_margin.idxmin()].reset_index(drop=True)

    timeFolder=f'{startTime[:2]}_{startTime[3:]}'
    marginsExists=os.path.exists("margins")
    timeExists=os.path.exists("margins/{}".format(timeFolder))
    if(not marginsExists):
        os.makedirs("margins")
    if(not timeExists):
        os.makedirs("margins/{}".format(timeFolder))

    df.to_csv('margins/{}/{}_margin.csv'.format(timeFolder,company), index=False)
    i+=1
    print('{}\nMargin Created for {}\n'.format(i,company))
print('Task completed')