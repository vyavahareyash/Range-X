import numpy as np 
import pandas as pd

data = pd.read_csv('tables/12_30/ADANIENT_data_table.csv')

size = data['Candle_size']
reversal = data['tReversal']
print(size.corr(reversal))
