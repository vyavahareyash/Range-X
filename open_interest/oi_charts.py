import os
# os.system("pip install --upgrade pandas")
# os.system("pip install --upgrade numpy")
# os.system("pip install --upgrade matlplotlib")
# os.system("pip install --upgrade seaborn")
# os.system("cls")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

source_file = 'record_analysis.txt'
source_folder_1 = 'z_flags_DEC_JAN'
source_folder_2 = 'z_flags_JAN_FEB'
destination_folder = "analysis_charts"

dataExists = os.path.exists(source_file) and os.path.exists(source_folder_1) and os.path.exists(source_folder_2)
if(dataExists):
    record_analysis = open(source_file, 'r')
    company_list = record_analysis.read().split()
else:
    exit('Data does not exists')

chartExists=os.path.exists(destination_folder)
if(not chartExists):
    os.makedirs(destination_folder)

def strip_date(date):
    return date[5:]

for company in company_list:
    try:
        data_1 = pd.read_excel(f"{source_folder_1}/{company}.xlsx")
        data_2 = pd.read_excel(f"{source_folder_2}/{company}.xlsx")
            
        data_1['Date'] = data_1.apply(lambda row: strip_date(row.Date),axis=1)
        data_2['Date'] = data_2.apply(lambda row: strip_date(row.Date),axis=1)
        
        plt.clf()
        plt.figure(figsize=(15,5))
        plt.plot(data_1['Date'], data_1['OI_Combined'],label = 'OI_DEC_JAN')
        plt.plot(data_2['Date'], data_2['OI_Combined'],label = 'OI_JAN_FEB')
        plt.xticks(rotation=90)
        plt.ylabel("Open Interest")
        plt.xlabel("Date =>")
        plt.legend()
        plt.title(f'{company}')
        plt.savefig(f'{destination_folder}/{company}.png',dpi=500)
        
    except Exception as e:
        print(str(e))