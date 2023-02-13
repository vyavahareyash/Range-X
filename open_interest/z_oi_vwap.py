import os
# os.system("pip install pandas")
# os.system("pip install numpy")
# os.system("pip install matlplotlib")
# os.system("pip install seaborn")
# os.system("pip install scipy")
# os.system("pip install PIL")
# os.system("cls")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
from PIL import Image

destination_folder = "z_oi_vwap_plots_JAN_FEB"
source_folder = "z_flags_JAN_FEB"

plotExists=os.path.exists(destination_folder)
if(not plotExists):
    os.makedirs(destination_folder)

dataExists=os.path.exists(source_folder)
if(dataExists):
    company_list = os.listdir(source_folder)
else:
    exit('Data does not exists')

def annotate(data, **kws):
    r, p = sp.stats.pearsonr(data['VWAP'], data['OI_Combined'])
    ax = plt.gca()
    ax.text(.05, .9, 'r={:.2f}, p={:.2g}'.format(r, p), transform=ax.transAxes)

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

gCount=0
rCount=0
gList=[]
rList=[]

# Demo list
# company_list=[]
# demo_list = ['BAJAJFINSV','BHARTIARTL','DRREDDY','KOTAKBANK','NATIONALUM','PAGEIND','PFC','RELIANCE','TVSMOTOR','ULTRACEMCO','UPL','WIPRO']
# for company in demo_list:
#     company_list.append(company+'.xlsx')

for company in company_list:
    try:
        data = pd.read_excel(f'{source_folder}/{company}')
        
        plt.clf()
        f1 = sns.lmplot(x='VWAP', y='OI_Combined', data=data)
        f1.map_dataframe(annotate)
        r1, p = sp.stats.pearsonr(data['VWAP'], data['OI_Combined'])
        plt.scatter(x='VWAP', y='OI_Combined', data=data[data['TotalFlag']>0],color='red')
        plt.title('{}'.format(company.split('.')[0]))
        plt.grid(color='lightgrey')
        plt.savefig(f'{destination_folder}/img1.png',dpi=500)
        
        data.drop(data[data['TotalFlag']>0].index,inplace=True)
        
        plt.clf()
        f2 = sns.lmplot(x='VWAP', y='OI_Combined', data=data)
        f2.map_dataframe(annotate)
        r2, p = sp.stats.pearsonr(data['VWAP'], data['OI_Combined'])
        if abs(r2) > abs(r1): 
            color='green'
            gCount+=1
            gList.append(company.split('.')[0])
        else: 
            color='red'
            rCount+=1
            rList.append(company.split('.')[0])
        plt.title('{} flags'.format(company.split('.')[0]),color=color)
        plt.grid(color='lightgrey')
        plt.savefig(f'{destination_folder}/img2.png',dpi=500)
        
        im1 = Image.open(f'{destination_folder}/img1.png')
        im2 = Image.open(f'{destination_folder}/img2.png')

        get_concat_h(im1, im2).save(f'{destination_folder}/{company.split(".")[0]}.png')
        plt.close()
        print('Plot created for {}'.format(company.split('.')[0]))
    
    except Exception as e:
        plt.clf()
        plt.close()
        print('Error occured for {}'.format(company.split('.')[0]))
        print(str(e))    

os.remove(f'{destination_folder}/img1.png')
os.remove(f'{destination_folder}/img2.png')

print('{} Charts show improved relation after removing flags\n{}\n{} Charts show decline in relation after removing flags\n{}'.format(gCount,gList,rCount,rList))
