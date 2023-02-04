import os
os.system("pip install pandas")
os.system("pip install numpy")
os.system("cls")

flagExists=os.path.exists("flags_2")
if(not flagExists):
    os.makedirs("flags_2")

import numpy as np
import pandas as pd

company_list = os.listdir('oi_data_2')

print("Fetching data for {} companies".format(len(company_list)))

j=1

for company in company_list:
    try:
        print('\n'+str(j)+')')
        j+=1
        data = pd.read_csv("oi_data_2/{}".format(company))
        n = len(data)
        data.drop(np.arange(n-5,n),inplace=True)

        delLow = data['PerDelivery'].quantile(0.05)
        delHigh = data['PerDelivery'].quantile(0.95)
        oiLow = data['Change_in_OI'].quantile(0.05)
        oiHigh = data['Change_in_OI'].quantile(0.95)
        vwapLow = data['Change_in_VWAP'].quantile(0.05)
        vwapHigh = data['Change_in_VWAP'].quantile(0.95)

        vwapFlag=[]
        oiFlag=[]
        delFlag = []
        for i in range(len(data)):
            if data.loc[i]['PerDelivery'] <= delLow or data.loc[i]['PerDelivery'] >= delHigh:
                delFlag.append(1)
            else:
                delFlag.append(0)
                
            if data.loc[i]['Change_in_OI'] <= oiLow or data.loc[i]['Change_in_OI'] >= oiHigh:
                oiFlag.append(1)
            else:
                oiFlag.append(0)
            
            if data.loc[i]['Change_in_VWAP'] <= vwapLow or data.loc[i]['Change_in_VWAP'] >= vwapHigh:
                vwapFlag.append(1)
            else:
                vwapFlag.append(0)
                
        data['DeliveryFlag'] = np.array(delFlag)
        data['OIFlag'] = np.array(oiFlag)
        data['VWAPFlag'] = np.array(vwapFlag)
        data['TotalFlag']=data['DeliveryFlag']+data['OIFlag']+data['VWAPFlag']
        data.to_csv('flags_2/{}'.format(company))
        print('Flags created for {}'.format(company))
        
    except Exception as e:
        print(str(e))