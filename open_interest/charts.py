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
    
company_list = os.listdir('oi_data')

for company in company_list:
    try:
        data = pd.read_csv("oi_data/{}".format(company))
        n = len(data)
        data.drop(np.arange(n-5,n),inplace=True)
        x=data[data['DeliveryFlag']>0]
        plt.scatter(data['Date'],data['PerDelivery'],color='blue')
        plt.scatter(x['Date'],x['PerDelivery'],color='red')
        plt.savefig('charts/{}.png'.format(company))
        
    except Exception as e:
        print(str(e))