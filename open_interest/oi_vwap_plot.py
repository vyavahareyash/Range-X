import os
os.system("pip install pandas")
os.system("pip install numpy")
os.system("pip install matlplotlib")
os.system("pip install seaborn")
os.system("pip install scipy")
os.system("pip install PIL")
os.system("cls")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
from PIL import Image

plotExists=os.path.exists("oi_vwap_plots")
if(not plotExists):
    os.makedirs("oi_vwap_plots")

dataExists=os.path.exists("oi_data")
if(dataExists):
    company_list = os.listdir('oi_data')
else:
    exit('Data does not exists')
    
def annotate(data, **kws):
    r, p = sp.stats.pearsonr(data['VWAP'], data['OI_Combined'])
    ax = plt.gca()
    ax.text(.05, .8, 'r={:.2f}, p={:.2g}'.format(r, p), transform=ax.transAxes)
    
def annotate_ma(data, **kws):
    r, p = sp.stats.pearsonr(data['VWAP_MA'], data['OI_Combined_MA'])
    ax = plt.gca()
    ax.text(.05, .8, 'r={:.2f}, p={:.2g}'.format(r, p),transform=ax.transAxes)

def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst
    
for company in company_list:
    try:
        data = pd.read_csv('oi_data/{}'.format(company))
        n = len(data)
        data.drop(np.arange(n-5,n),inplace=True)
        
        window_size=5
        data['VWAP_MA'] = data['VWAP'].rolling(window=window_size,center=True).mean()
        data['OI_Combined_MA'] = data['OI_Combined'].rolling(window=window_size,center=True).mean()
        data.dropna(subset=['VWAP_MA','OI_Combined_MA'],inplace=True)
        
        plt.clf()
        f1 = sns.lmplot(x='VWAP', y='OI_Combined', data=data)
        f1.map_dataframe(annotate)
        plt.title('{} VWAP vs OI'.format(company.split('.')[0].split('_')[2]))
        plt.savefig('oi_vwap_plots/img1.png')
        
        plt.clf()
        f2 = sns.lmplot(x='VWAP_MA', y='OI_Combined_MA', data=data)
        f2.map_dataframe(annotate_ma)
        plt.title('{} VWAP vs OI (MA)'.format(company.split('.')[0].split('_')[2]))
        plt.savefig('oi_vwap_plots/img2.png')
        plt.clf()
        
        im1 = Image.open('oi_vwap_plots/img1.png')
        im2 = Image.open('oi_vwap_plots/img2.png')

        get_concat_h(im1, im2).save('oi_vwap_plots/{}.png'.format(company.split('.')[0].split('_')[2]))
        print('Plot created for {}'.format(company.split('.')[0].split('_')[2]))
    
    except Exception as e:
        print('Error occured for {}'.format(company.split('.')[0].split('_')[2]))
        print(str(e))    

os.remove('oi_vwap_plots/img1.png')
os.remove('oi_vwap_plots/img2.png')
