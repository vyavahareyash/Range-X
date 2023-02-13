import os
os.system("pip install pandas")
os.system("pip install numpy")
os.system("pip install matlplotlib")
os.system("pip install seaborn")
os.system("cls")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

chartExists=os.path.exists("charts")
if(not chartExists):
    os.makedirs("charts")
    
company_list = os.listdir('../../../Python notebooks/YT_Sandbox/Yash/send')

for company in company_list:
    try:
        data = pd.read_csv("oi_data_2/{}".format(company))
        # n = len(data)
        # data.drop(np.arange(n-5,n),inplace=True)
        # x=data[data['DeliveryFlag']>0]
        # plt.scatter(data['Date'],data['PerDelivery'],color='blue')
        # plt.scatter(x['Date'],x['PerDelivery'],color='red')
        # plt.savefig('charts/{}.png'.format(company))

        # plt.ylim([100000,1000000000])
        plt.plot(data['Date'],data['OI_Combined'])
        plt.savefig('charts/OI_{}.png'.format(company))
        plt.clf()
        # plt.ylim([0,10000])
        plt.plot(data['Date'],data['VWAP'])
        plt.savefig('charts/VWAP_{}.png'.format(company))
        plt.clf()
        
    except Exception as e:
        plt.clf()
        print(str(e))