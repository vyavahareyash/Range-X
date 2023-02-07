import os
# os.system("pip install --upgrade pandas")
# os.system("pip install --upgrade numpy")
# os.system("pip install --upgrade matlplotlib")
# os.system("pip install --upgrade seaborn")
# os.system("pip install --upgrade math")
# os.system("pip install --upgrade scipy")
os.system("cls")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import scipy as sp

chartExists=os.path.exists("z_out_charts")
if(not chartExists):
    os.makedirs("z_out_charts")
    
dataExists=os.path.exists("z_flags")
if(dataExists):
    company_list = os.listdir('z_flags')
else:
    exit('Data does not exists')
    
delList=[]
oiList=[]
vwapList=[]

for company in company_list:
    data = pd.read_excel('z_flags/{}'.format(company))
    
    delList.extend(data['PerDelivery'].dropna().tolist())
    oiList.extend(data['Change_in_OI'].dropna().tolist())
    vwapList.extend(data['Change_in_VWAP'].dropna().tolist())
    
delMax = math.ceil(max(delList)/10)*10
delMin = math.floor(min(delList)/10)*10
oiMax = math.ceil(max(oiList)/10)*10
oiMin = math.floor(min(oiList)/10)*10
vwapMax = math.ceil(max(vwapList)/10)*10
vwapMin = math.floor(min(vwapList)/10)*10

pthreshold = 1.5
nthreshold = -1.5

def annotate_del(data, **kws):
    r, p = sp.stats.pearsonr(data['index'], data['PerDelivery'])
    ax = plt.gca()
    ax.text(.05, .9, 'r={:.2f}, p={:.2g}'.format(r, p), transform=ax.transAxes)
    
def annotate_oi(data, **kws):
    r, p = sp.stats.pearsonr(list(data['Change_in_OI'].dropna().index), data['Change_in_OI'].dropna())
    ax = plt.gca()
    ax.text(.05, .9, 'r={:.2f}, p={:.2g}'.format(r, p), transform=ax.transAxes)
    
def annotate_vwap(data, **kws):
    r, p = sp.stats.pearsonr(list(data['Change_in_VWAP'].dropna().index), data['Change_in_VWAP'].dropna())
    ax = plt.gca()
    ax.text(.05, .9, 'r={:.2f}, p={:.2g}'.format(r, p), transform=ax.transAxes)
    
for company in company_list:
    try:
        data = pd.read_excel("z_flags/{}".format(company))
        # n = len(data)
        # data.drop(np.arange(n-5,n),inplace=True)
        
        data['index'] = data.index
        
        delUB = (pthreshold * data['PerDelivery'].std()) + data['PerDelivery'].mean() 
        oiUB = (pthreshold * data['Change_in_OI'].std()) + data['Change_in_OI'].mean()
        vwapUB = (pthreshold * data['Change_in_VWAP'].std()) + data['Change_in_VWAP'].mean()
        delLB =  (nthreshold * data['PerDelivery'].std()) + data['PerDelivery'].mean()
        oiLB = (nthreshold * data['Change_in_OI'].std()) + data['Change_in_OI'].mean()
        vwapLB = (nthreshold * data['Change_in_VWAP'].std()) + data['Change_in_VWAP'].mean()
        
        delM = data['PerDelivery'].mean()
        oiM = data['Change_in_OI'].mean()
        vwapM = data['Change_in_VWAP'].mean()
                
        plt.clf()
        f_data=data[abs(data['DeliveryFlag'])>0]
        f_x=list(f_data.index)
        data.drop(index=f_x,inplace=True)
        g = sns.lmplot(x='index',y='PerDelivery',data=data)
        plt.ylim([delMin,delMax])
        plt.scatter(data['index'],data['PerDelivery'],color='blue')
        plt.scatter(f_x,f_data['PerDelivery'],color='red',marker='*')
        plt.plot(data['index'],np.ones(len(data))*delUB,color='pink',linestyle='dashed',label='Upper bound = {}'.format(round(delUB,2)))
        plt.plot(data['index'],np.ones(len(data))*delLB,color='pink',linestyle='dashed', label='Lower bound = {}'.format(round(delLB,2)))
        plt.plot(data['index'],np.ones(len(data))*delM,color='lightblue',linestyle='dashed', label='Mean = {}'.format(round(delM,2)))
        plt.grid(color='lightgrey')
        g.map_dataframe(annotate_del)
        plt.legend()
        plt.title('{}'.format(company.split('.')[0]))
        plt.savefig('z_out_charts/Delivery_{}.png'.format(company.split('.')[0]),dpi=500)
        
        plt.clf()
        f_data=data[abs(data['OIFlag'])>0]
        f_x=list(f_data.index)
        data.drop(index=f_x,inplace=True)
        g = sns.lmplot(x='index',y='Change_in_OI',data=data)
        plt.ylim([oiMin,oiMax])
        plt.scatter(data['index'],data['Change_in_OI'],color='blue')
        plt.scatter(f_x,f_data['Change_in_OI'],color='red')
        plt.plot(data['index'],np.ones(len(data))*oiUB,color='pink',linestyle='dashed',label='Upper bound = {}'.format(round(oiUB,2)))
        plt.plot(data['index'],np.ones(len(data))*oiLB,color='pink',linestyle='dashed', label='Lower bound = {}'.format(round(oiLB,2)))
        plt.plot(data['index'],np.ones(len(data))*oiM,color='lightblue',linestyle='dashed', label='Mean = {}'.format(round(oiM,2)))
        plt.grid(color='lightgrey')
        g.map_dataframe(annotate_oi)
        plt.legend()
        plt.title('{}'.format(company.split('.')[0]))
        plt.savefig('z_out_charts/OI_{}.png'.format(company.split('.')[0]),dpi=500)

        plt.clf()
        f_data=data[abs(data['VWAPFlag'])>0]
        f_x=list(f_data.index)
        data.drop(index=f_x,inplace=True)
        g = sns.lmplot(x='index',y='Change_in_VWAP',data=data)
        plt.ylim([vwapMin,vwapMax])
        plt.scatter(data['index'],data['Change_in_VWAP'],color='blue')
        plt.scatter(f_x,f_data['Change_in_VWAP'],color='red')
        plt.plot(data['index'],np.ones(len(data))*vwapUB,color='pink',linestyle='dashed',label='Upper bound = {}'.format(round(vwapUB,2)))
        plt.plot(data['index'],np.ones(len(data))*vwapLB,color='pink',linestyle='dashed', label='Lower bound = {}'.format(round(vwapLB,2)))
        plt.plot(data['index'],np.ones(len(data))*vwapM,color='lightblue',linestyle='dashed', label='Mean = {}'.format(round(vwapM,2)))
        plt.grid(color='lightgrey')
        g.map_dataframe(annotate_vwap)
        plt.legend()
        plt.title('{}'.format(company.split('.')[0]))
        plt.savefig('z_out_charts/VWAP_{}.png'.format(company.split('.')[0]),dpi=500)
        plt.clf()
        plt.close()
        
        print('Charts created for {}'.format(company.split('.')[0]))
        
    except Exception as e:
        plt.clf()
        plt.close
        print(str(e))