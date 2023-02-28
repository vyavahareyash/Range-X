def get_table(company,startTime,timeFolder):
    import numpy as np
    import pandas as pd

    dataset=pd.read_csv('data/{}.csv'.format(company))
    
    dataset['Date'] = [ x.split(' ')[0] for x in dataset['datetime'].tolist() ]
    dataset['Time'] = [ x.split(' ')[1] for x in dataset['datetime'].tolist() ]

    hh = int(startTime.split(':')[0])
    mm = int(startTime.split(':')[1])
    
    # Remove the candles before start time
    for i in range(len(dataset)):
        dFlag=0
        if(int(dataset['Time'][i][0:2])<hh):
            dFlag=1
        if(int(dataset['Time'][i][0:2])==hh and int(dataset['Time'][i][3:5])<mm):
            dFlag=1
        if dFlag==1:
            dataset.drop(i,inplace=True)
    #time variable
#     print(dataset)
    dataset.reset_index(inplace=True,drop=True)

    cols=['Date','S_Window','Candle_size','pDelta','nDelta','tReversal']
    table = pd.DataFrame(columns=cols)

    i=0
    j=0
    k=0
    dayset=[]
    #Create day sets
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

    #Gets candle type
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
    pMos=0
    nMos=0

    
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

    table.to_csv("tables/{}/{}_table.csv".format(timeFolder,company),index=False)
    # os.system("cls")
    print("Table created for {}\n".format(company))

