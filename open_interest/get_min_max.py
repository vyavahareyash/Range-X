import sys
import os
import math
# import numpy as np
import pandas as pd

company_list = os.listdir('z_flags')

delList=[]
oiList=[]
vwapList=[]

for company in company_list:
    data = pd.read_excel('z_flags/{}'.format(company))
    # data.dropna(subset=['Change_in_OI','Change_in_VWAP'])
    
    delList.extend(data['PerDelivery'].dropna().tolist())
    oiList.extend(data['Change_in_OI'].dropna().tolist())
    vwapList.extend(data['Change_in_VWAP'].dropna().tolist())
    
delMax = math.ceil(max(delList)/10)*10
delMin = math.floor(min(delList)/10)*10
oiMax = math.ceil(max(oiList)/10)*10
oiMin = math.floor(min(oiList)/10)*10
vwapMax = math.ceil(max(vwapList)/10)*10
vwapMin = math.floor(min(vwapList)/10)*10

# print(vwapList)
# print(oiList)

print('delMax = {}\ndelMin = {}\n\noiMax = {}\noiMin = {}\n\nvwapMax = {}\nvwapMin = {}\n\n'.format(delMax,delMin,oiMax,oiMin,vwapMax,vwapMin))

# company = 'ACC.xlsx'
# data = pd.read_excel('z_flags/{}'.format(company))
# delList.append()
# print(delList)