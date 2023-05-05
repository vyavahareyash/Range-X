import pandas as pd
from tvDatafeed import TvDatafeed, Interval
tv = TvDatafeed()

def getData(list): # Pass list of companies 
    itemNo=1
    fetchedCount = 0
    failCount=0 
    successList = []
    failedList = []
    
    for company in list:
        try:
            # os.system("cls")
            print(str(itemNo)+')')
            itemNo+=1
            print('fetching data for '+company)
            data_stocks = tv.get_hist(symbol=company,exchange='NSE',interval=Interval.in_15_minute,n_bars=90000)
            data_stocks.to_csv("data/"+company+"_data.csv")
            fetchedCount += 1 
            print('Successfully fetched {} data'.format(company))
            successList.append(company+"_data")
            
        except Exception as e:
            failCount+=1
            failedList.append(company)
            print(str(e)+'\n')
            
        finally:
            print('Fetch count = {}'.format(fetchedCount))
            print('Fail count = {}\n'.format(failCount))
            
    # os.system("cls")
    return successList, failedList
