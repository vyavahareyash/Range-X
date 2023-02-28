import os
os.system("pip install numpy")
os.system("pip install pandas")

import numpy as np
import pandas as pd

sourceFolder = 'data'
destinationFolder = 'target_pred'

#variables
startTime="10:15"
pMos = 2
nMos = 4

dataExists = os.path.exists(sourceFolder)
if(dataExists):
    companyList = os.listdir(sourceFolder)
else:
    exit("Data does not exist")

destinationExists = os.path.exists(destinationFolder)
if(not destinationExists):
    os.mkdir(destinationFolder)
    
#demo list
companyList = ["RELIANCE_data.csv"]


def get_targets():
    
    pass


for company in companyList:
    data = pd.read_csv(sourceFolder +"/"+ company)
    table = get_targets(data)
