# This script parses, formats and concats all data from .txt files in data folder
# Once reformatted data is then exported to excel file 

from __future__ import division
import pandas as pd
import numpy as np
import sys, os, math
from scipy import stats
import matplotlib.pyplot as plt

#print 'Python Version: ', sys.version
#print 'Pandas Version: ', pd.__version__

# Directory
os.getcwd()
path = 'C:\Users\lab-user\Desktop\AudioVisMotionRatchetExp\data_200\\' # path for 200 msec data
#path = 'C:\\Users\\lab-user\\Desktop\\AudioVisMotionRatchetExp\\250_Exp_data' # path for 250 msec data
os.chdir(path)

# Retrieves the data files from the master folder
def GetFile(path, startID):
    FileNames = []
    for files in os.listdir("."):
        if files.startswith(startID): # change to single subject
            FileNames.append(files)
    return FileNames
    
 
    # converts each data file into a pandas data frame        
def GetData(fnombre):   
    #     idx = range(1,451)
    # Parse the data file
    # 0 = first sheet
    df = pd.read_csv(fnombre, header=9, sep=' ', error_bad_lines=False)
    
    # Tag record to file name
    #df['File'] = fnombre
    df.insert(0,'p',int(fnombre[16:19]))
#     df['p'] = int(fnombre[16:19])
    #df['Block'] = 1
    # Make the "File" column the index of the df
    return df.set_index(['p'])
  
# Reformat files into list of Data Frames
def dfList(dataList):
    df_list = [GetData(fname) for fname in dataList]
    return df_list 

# concatenates all dataframes into one big data frame
def bigDataFrame(dfs): 
    bigdf = pd.concat(dfs[:])
    #bigdf = pd.concat(dfs[16:])
    return bigdf
# Parse and Reformat Data   
data = GetFile(path, "AVMotion_subject") # extracts files from folder
dfs = dfList(data)#converts to list of data frames
big_df = bigDataFrame(dfs) # concat all df in dfs to one data frame

# Write data to excel file
writer = pd.ExcelWriter('AvMotionData_200.xlsx')
big_df.to_excel(writer,'Sheet1')
writer.save()