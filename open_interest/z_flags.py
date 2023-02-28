import os
# os.system("pip install pandas")
# os.system("pip install numpy")
# os.system("pip install warnings")
# os.system("pip install jinja2")
# os.system("pip install openpyxl")
# os.system("cls")

# destination_folder = "z_flags_DEC_JAN"
# source_folder = "oi_data_DEC_JAN"

destination_folder = "z_flags_JAN_FEB"
source_folder = "oi_data_JAN_FEB"

flagExists=os.path.exists(destination_folder)
if(not flagExists):
    os.makedirs(destination_folder)

import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

dataExists=os.path.exists(source_folder)
if(dataExists):
    company_list = os.listdir(source_folder)
else:
    exit('Data does not exists')
    
print("Creating flags for {} companies".format(len(company_list)))

def color_green(column):
    pos = 'background-color: green'
    default = ''
    
    return [pos if v > 0 else default for v in column]

def color_red(column):
    neg = 'background-color: red'
    default = ''
    
    return [neg if v < 0 else default for v in column]

def color_yellow(column):
    neg = 'background-color: yellow'
    default = ''
    
    return [neg if v > 0 else default for v in column]

j=1

for company in company_list:
    try:
        print('\n'+str(j)+')')
        j+=1
        data = pd.read_csv(f"{source_folder}/{company}")
        n = len(data)
        data.drop(np.arange(n-5,n),inplace=True)
        mean = data.mean()
        std = data.std()
        
        data['z_oi'] = (data['Change_in_OI']-mean['Change_in_OI']) / std['Change_in_OI']
        data['z_del'] = (data['PerDelivery']-mean['PerDelivery']) / std['PerDelivery']
        data['z_vwap'] = (data['Change_in_VWAP']-mean['Change_in_VWAP']) / std['Change_in_VWAP']

        pthreshold = 1.5
        nthreshold = -1.5
        
        vwapFlag=[]
        oiFlag=[]
        delFlag = []

        for i in range(len(data)):
            if data.loc[i]['z_del'] >= pthreshold:
                delFlag.append(1)
            elif data.loc[i]['z_del'] <= nthreshold:
                delFlag.append(-1)
            else:
                delFlag.append(0)
                
            if data.loc[i]['z_oi'] >= pthreshold:
                oiFlag.append(1)
            elif data.loc[i]['z_oi'] <= nthreshold:
                oiFlag.append(-1)
            else:
                oiFlag.append(0)
                
            if data.loc[i]['z_vwap'] >= pthreshold:
                vwapFlag.append(1)
            elif data.loc[i]['z_vwap'] <= nthreshold:
                vwapFlag.append(-1)
            else:
                vwapFlag.append(0)
                
        data['OIFlag'] = np.array(oiFlag)
        data['VWAPFlag'] = np.array(vwapFlag)
        data['DeliveryFlag'] = np.array(delFlag)
        
        data['TotalFlag']=abs(data['DeliveryFlag'])+abs(data['OIFlag'])+abs(data['VWAPFlag'])
        
        data = data.loc[:,['Date', 'Symbol', 'Open Interest', 'Open Interest.1', 'OI_Combined', 'VWAP', 'Volume', 'Change_in_Volume', 'Delivery', 'Change_in_OI', 'OIFlag', 'z_oi', 'Change_in_VWAP', 'VWAPFlag', 'z_vwap', 'PerDelivery', 'DeliveryFlag', 'z_del', 'TotalFlag']]
        
        data.style.apply(color_red, subset=['OIFlag', 'VWAPFlag', 'DeliveryFlag'], 
                    axis=0).apply(color_green, subset=['OIFlag', 'VWAPFlag', 'DeliveryFlag'],
                                    axis=0).apply(color_yellow, subset=['TotalFlag'],
                                                  axis=0).to_excel('{}/{}.xlsx'.format(destination_folder,company.split('.')[0].split('_')[0]), index = False)
        
        print('Flags created for {}'.format(company.split('.')[0].split('_')[0]))
                
    except Exception as e:
        print(str(e))

