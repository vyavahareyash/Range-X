import os
# os.system("pip install pandas")
# os.system("pip install numpy")
# os.system("pip install matlplotlib")
# os.system("pip install seaborn")
# os.system("pip install scipy")
# os.system("pip install PIL")
os.system("cls")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
from PIL import Image

plotExists=os.path.exists("z_oi_vwap_plots")
if(not plotExists):
    os.makedirs("z_oi_vwap_plots")

dataExists=os.path.exists("z_flags")
if(dataExists):
    company_list = os.listdir('z_flags')
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

for company in company_list:
    try:
        data = pd.read_excel('z_flags/{}'.format(company))
        
        plt.clf()
        f1 = sns.lmplot(x='VWAP', y='OI_Combined', data=data)
        f1.map_dataframe(annotate)        
        plt.scatter(x='VWAP', y='OI_Combined', data=data[data['TotalFlag']>0],color='red')
        plt.title('{}'.format(company.split('.')[0]))
        plt.grid(color='lightgrey')
        plt.savefig('z_oi_vwap_plots/img1.png',dpi=500)
        
        data.drop(data[data['TotalFlag']>0].index,inplace=True)
        
        plt.clf()
        f2 = sns.lmplot(x='VWAP', y='OI_Combined', data=data)
        f2.map_dataframe(annotate)
        plt.title('{} flags'.format(company.split('.')[0]))
        plt.grid(color='lightgrey')
        plt.savefig('z_oi_vwap_plots/img2.png',dpi=500)
        
        im1 = Image.open('z_oi_vwap_plots/img1.png')
        im2 = Image.open('z_oi_vwap_plots/img2.png')

        get_concat_h(im1, im2).save('z_oi_vwap_plots/{}.png'.format(company.split('.')[0]))
        plt.close()
        print('Plot created for {}'.format(company.split('.')[0]))
    
    except Exception as e:
        plt.clf()
        plt.close()
        print('Error occured for {}'.format(company.split('.')[0]))
        print(str(e))    

os.remove('z_oi_vwap_plots/img1.png')
os.remove('z_oi_vwap_plots/img2.png')
