import numpy as np
import pandas as pd
import os

def get_table_count(company,startTime,pMos,nMos):

    dataset=pd.read_csv('data/{}_data.csv'.format(company))
    
    dataset['Date'] = [ x.split(' ')[0] for x in dataset['datetime'].tolist() ]
    dataset['Time'] = [ x.split(' ')[1] for x in dataset['datetime'].tolist() ]

    hh = int(startTime.split(':')[0])
    mm = int(startTime.split(':')[1])
    
    for i in range(len(dataset)):
        dFlag=0
        if(int(dataset['Time'][i][0:2])<hh):
            dFlag=1
        if(int(dataset['Time'][i][0:2])==hh and int(dataset['Time'][i][3:5])<mm):
            dFlag=1
        if dFlag==1:
            dataset.drop(i,inplace=True)

    dataset.reset_index(inplace=True,drop=True)

    cols=['Date','S_Window','Candle_size','pDelta','nDelta','tReversal']
    table = pd.DataFrame(columns=cols)

    i=0
    j=0
    k=0
    dayset=[]
    while(i<len(dataset)-1):
        currDate=dataset['Date'][i]
        nextDate=dataset['Date'][i+1]
        while(currDate==nextDate):
            if(i==len(dataset)-2):
                i+=1
                break
            i+=1
            currDate=dataset['Date'][i]
            nextDate=dataset['Date'][i+1]
        i+=1
        dayset.append(dataset[j:i][:])
        j=i
        k+=1
    dayset.append(dataset[j:][:])

    def candle_type(upperBound,lowerBound,high,low):
        if (high <= upperBound and low >= lowerBound):
            return 1
        elif (high > upperBound and low >= lowerBound):
            return 2
        elif (high <= upperBound and low < lowerBound):
            return 3
        elif (low >= upperBound):
            return 2
        elif (high <= lowerBound):
            return 3
        elif (high > upperBound and low < lowerBound):
            return 6
        else:
            return 0

    totalDays=len(dayset)

    #day no.
    day=0

    for day in range(totalDays-1):

        #start index of day
        si=dayset[day].index[0]

        #end index of day
        ei=dayset[day].index[0]+len(dayset[day])

        selectedCandle=dayset[day].loc[si]

        date=selectedCandle['Date']
        high=float(selectedCandle['high'])
        low=float(selectedCandle['low'])
        upperBound=high+pMos
        lowerBound=low-nMos
        sw=f'{lowerBound}-{upperBound}'
        candle_size = abs(high-low)

        pDelta = max(dayset[day]['high']) - upperBound
        nDelta = lowerBound - min(dayset[day]['low'])
        typearr=[]

        for i in range(si,ei):
            high=float(dayset[day]['high'][i])
            low=float(dayset[day]['low'][i])
            type = candle_type(upperBound,lowerBound,high,low)
            typearr.append(type)

        tr=0
        pattern1=[2,3]
        pattern2=[3,2]
        pattern3=[2,6]
        pattern4=[3,6]
        for j in range(len(typearr)-1):
            if((typearr[j:j+2]==pattern1)or(typearr[j:j+2]==pattern2)or(typearr[j:j+2]==pattern3)or(typearr[j:j+2]==pattern4)):
                tr+=1

        table.loc[day]=[date,sw,candle_size,pDelta,nDelta,tr]

    count = len(table[table['tReversal']!=0])
    return count

df = pd.DataFrame(columns=['pMos','nMos','count'])

company='RELIANCE'
startTime='10:15'
pMosList=nMosList = np.arange(10)

plist=[]
nlist=[]
clist=[]
for pMos in pMosList:
    for nMos in nMosList:
        count = get_table_count(company,startTime,pMos,nMos)
        plist.append(pMos)
        nlist.append(nMos)
        clist.append(count)
df['pMos']=np.array(plist)
df['nMos']=np.array(nlist)
df['total_reversals']=np.array(clist)

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

df.to_csv('margins/{}/{}_margin.csv'.format(timeFolder,company))
print('Task completed')