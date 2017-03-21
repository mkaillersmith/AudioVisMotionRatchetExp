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
path = 'C:\Users\lab-user\Desktop\AudioVisMotionRatchetExp\data'
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
    df['Subject'] = int(fnombre[16:19])
    #df['Block'] = 1
    # Make the "File" column the index of the df
    return df.set_index(['Trial'])
  
        
# Reformat files into list of Data Frames
def dfList(dataList):
    df_list = [GetData(fname) for fname in dataList]
    return df_list
     
def groupSound(dfs):
    for i in range(len(dfs)):
        snd_df = dfs[i].groupby(['Sound'])
    return snd_df

def getMean(df):  
    mean_snd = []   
    for i in snd_df['RT'].mean():
        mean_snd.append(i)
    return mean_snd
 
def stdDeviation(snd_df):  
    stdDev_lst = []   
    for i in snd_df['RT'].std():
        stdDev_lst.append(i)
    return stdDev_lst    
       
def std_error(df): # This function takes a list of dictionaries containing subjects overall percent coorect by block then calculates the overall standard error
    stdError_lst = []
    for i in range(1,4): # for each of the three conditons
        phase = df['Sound'] == i
        phase_df = df[phase]
        stdError = stats.sem(phase_df['RT'], ddof=0)
        stdError_lst.append(stdError)
    return stdError_lst

def all_std_error(dfs):
    stdMasterList = []
    for i in range(len(dfs)):
        stdError = std_error(dfs[i])
        stdMasterList.append(stdError)
    return stdMasterList        

def plotRT(mean, std_Error, title=' '):
    
    N = 3


    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, mean, width, color='blue', yerr=std_Error, ecolor='black')
    rects1[0].set_color('red')
    rects1[1].set_color('green')
    # add some text for labels, title and axes ticks
    ax.set_ylabel('RT')
    ax.set_title('MAE')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(('In Phase', 'Out Phase', 'No Sound'))
    plt.ylim(0,8)
    plt.title(title)
    


#    fig, ax = plt.subplots(figsize=(20, 10))
#    labels = ['In Phase', 'Out Phase', 'No Sound']
#    index = [1.0, 2.0, 3.0]
#    bar_width = 0.30
#    opacity = 0.4
#    
#    rects1 = plt.bar(index, mean, bar_width, alpha=opacity, color='blue', yerr=std_Error)
#
#    plt.xlabel('Sound')
#    plt.ylabel('RT')
#    plt.title('Motion After Effect')
#    ax.set_xticks(index + bar_width / 2)
#    ax.set_xticklabels(('In Phase', 'Out Phase', 'No Sound'))
#    plt.legend()
#
#    plt.tight_layout()
    plt.show()


snd_df = groupSound(dfs)
for i in range(len(dfs)):
    mean_snd = getMean(dfs[i])
    stdError = std_error(dfs[i])
    plotRT(mean_snd,stdError, title="subject "+str(i+1))
    print ''
    print 'subject'+str(i+1)
    print 'in phase mean = ', mean_snd[0]
    print 'in phase std error = ', stdError[0]
    print 'out phase mean = ', mean_snd[1]
    print 'out phase error = ', stdError[1]
    print 'no sound = ', mean_snd[2]
    print 'no sound = ', stdError[2]
    print ''






