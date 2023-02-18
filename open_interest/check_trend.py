import os
import numpy as np
import pandas as pd
import scipy as sp

source_folder_1 = 'z_flags_DEC_JAN'
source_folder_2 = 'z_flags_JAN_FEB'
destination_folder = 'trend_analysis'

sourceExists = os.path.exists(source_folder_1) and os.path.exists(source_folder_2)
if sourceExists:
    source_set_1 = set(os.listdir(source_folder_1))
    source_set_2 = set(os.listdir(source_folder_2))
    company_list = source_set_1.intersection(source_set_2)
else:
    exit('Data does not exists')
    
destExists = os.path.exists(destination_folder)
if not destExists:
    os.makedirs(destination_folder)
    
stock_list = []
fd_1_list = []
fd_2_list = []
tf_1_list = []
tf_2_list = []
r1_list = []
r2_list = []
# r1_f_list = []
# r2_f_list = []

for company in company_list:
    try:
        data_1 = pd.read_excel(f'{source_folder_1}/{company}')
        data_2 = pd.read_excel(f'{source_folder_2}/{company}')
        
        # Data 1
        falggedDays_1 = len(data_1[data_1['TotalFlag']>0])
        totalFlags_1 = sum(data_1['TotalFlag'])
        
        r1, p1 = sp.stats.pearsonr(data_1['VWAP'], data_1['OI_Combined'])
        
        # data_1.drop(data_1[data_1['TotalFlag']>0].index,inplace=True)

        # r1_f, p1_f = sp.stats.pearsonr(data_1['VWAP'], data_1['OI_Combined'])
        
        # Data 2
        falggedDays_2 = len(data_2[data_2['TotalFlag']>0])
        totalFlags_2 = sum(data_2['TotalFlag'])
        
        r2, p2 = sp.stats.pearsonr(data_2['VWAP'], data_2['OI_Combined'])
        
        # data_2.drop(data_2[data_2['TotalFlag']>0].index,inplace=True)
        
        # r2_f, p2_f = sp.stats.pearsonr(data_2['VWAP'], data_2['OI_Combined'])
        
        stock_list.append(company.split('.')[0])
        fd_1_list.append(falggedDays_1)
        fd_2_list.append(falggedDays_2)
        tf_1_list.append(totalFlags_1)
        tf_2_list.append(totalFlags_2)
        r1_list.append(r1)
        r2_list.append(r2)
        # r1_f_list.append(r1_f)
        # r2_f_list.append(r2_f)
        
        print(f'Trend analysed for {company.split(".")[0]}')
        
    except Exception as e:
        print(f'Failed for {company.split(".")[0]}')
        print(str(e))

df = pd.DataFrame()

df['company'] = stock_list
df['flaggedDays_1'] = fd_1_list
df['flaggedDays_2'] = fd_2_list
df['totalFlags_1'] = tf_1_list
df['totalFlags_2'] = tf_2_list
df['r_1'] = r1_list
df['r_2'] = r2_list
# df['r_1_f'] = r1_f_list
# df['r_2_f'] = r2_f_list
df['strong_corr'] = abs(df['r_1'])>0.7
df['stable_corr'] = abs(df['r_1'] - df['r_2']) <= 0.2
df['strong_stable'] = df.apply(lambda row: row.strong_corr and row.stable_corr,axis=1)
df.sort_values(by='company',inplace=True)

focus_list = list(df[df['strong_stable']]['company'])   #list of companies to focus

if (not os.path.exists('record_analysis.txt')):     #create text file if not exists already
    open('record_analysis.txt', 'x')                #store company names in text file
open('record_analysis.txt','w').close()             #clear the contents of text file
record_analysis = open('record_analysis.txt', 'w')  #open text file in write mode

for i in focus_list:                                #add each company in list to text file
    record_analysis.write(str(i)+' ')

df.to_excel(f'{destination_folder}/{source_folder_1.split("_")[2]}_{source_folder_2.split("_")[3]}_analysis.xlsx',index=False)
