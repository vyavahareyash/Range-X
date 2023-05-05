import numpy as np
import pandas as pd

company_list = open('companies_list.txt','r').read().split()
data={
    'Name':company_list,
    'pMos':np.zeros(len(company_list)),
    'nMos':np.zeros(len(company_list))
}

df = pd.DataFrame(data)

df.to_csv('NPvals.csv',index=False)