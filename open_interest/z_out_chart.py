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

chartExists=os.path.exists("z_out_charts")
if(not chartExists):
    os.makedirs("z_out_charts")
    
dataExists=os.path.exists("z_flags")
if(dataExists):
    company_list = os.listdir('z_flags')
else:
    exit('Data does not exists')
    

    
for company in company_list:
    try:
        data = pd.read_excel("z_flags/{}".format(company))
        # n = len(data)
        # data.drop(np.arange(n-5,n),inplace=True)
        
        plt.clf()
        plt.ylim([0,90])
        x=data[abs(data['DeliveryFlag'])>0]
        plt.scatter(data['Date'],data['PerDelivery'],color='blue')
        plt.scatter(x['Date'],x['PerDelivery'],color='red')
        plt.savefig('z_out_charts/Delivery_{}.png'.format(company.split('.')[0]))
        
        plt.clf()
        plt.ylim([-60,30])
        x=data[abs(data['OIFlag'])>0]
        plt.scatter(data['Date'],data['Change_in_OI'],color='blue')
        plt.scatter(x['Date'],x['Change_in_OI'],color='red')
        plt.savefig('z_out_charts/OI_{}.png'.format(company.split('.')[0]))

        plt.clf()
        plt.ylim([-10,20])
        x=data[abs(data['VWAPFlag'])>0]
        plt.scatter(data['Date'],data['Change_in_VWAP'],color='blue')
        plt.scatter(x['Date'],x['Change_in_VWAP'],color='red')
        plt.savefig('z_out_charts/VWAP_{}.png'.format(company.split('.')[0]))
        plt.clf()
        
        print('Charts created for {}'.format(company.split('.')[0]))
        
    except Exception as e:
        plt.clf()
        print(str(e))