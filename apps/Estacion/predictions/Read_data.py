#!/usr/bin/env python
# coding: utf-8

# ### Read meteorological data
# Folder with [original data](https://drive.google.com/drive/folders/1me2IpDY3om6IRKv_WMT5W6Qw0r9DI74C)

# In[1]:


import os
import zipfile
import pandas as pd
import glob
#import keplergl
#import geopandas as gpd
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import re
import numpy as np
from IPython import get_ipython
#from pyproj import Proj
get_ipython().run_line_magic('run', 'Meteo_utils.ipynb')


# In[ ]:


os.listdir('data')


# ## Automate data extraction from Drive downloads

# In[40]:


path = '/Users/tamarahuete/Documents/Github_repos/TFM21/data/RAW'
ziplist = glob.glob(f'{path}/*.zip')
#ziplist = glob.glob(f'data/*.zip')


# In[41]:


ziplist


# In[5]:


folder = 0


# In[9]:


zf = zipfile.ZipFile(f'{ziplist[folder]}')
zf.namelist()[0:10]


# In[10]:


### exclude macos files (only if copying data if using Drive directly these don't appear)
r = re.compile('^__MACOSX') # only csv files
exclude = list(filter(r.match, zf.namelist()[0:10])) 
clean = list(set(zf.namelist()[0:10])-set(exclude))


# In[12]:


files_by_date = order_meteo_zip(path, folder =folder)


# In[309]:


files_by_date


# In[14]:


df = read_meteo_csv(path =path,folder = folder,file = files_by_date[0])


# In[15]:


df.head()


# In[16]:


files_by_date[0].split('/')[-1].replace(" ","")


# In[105]:


station = files_by_date[0].split('/')[0].replace(" ","").replace(".","")
all_var = get_unique_variables(files_by_date,path =path,folder = folder)


# In[17]:


## Variable names:
# BAT  is  battery
# Not very clear: 'H_M Min','WindMnSpdSclr','WindMnSpdS','WindMnDirUnit'

replace_values ={
# Temperature
    'ATAvg' : ['AT1HrAvg', 'AT5minAvg', 'ATAvg','Temperatura'],
    'ATMin' : ['AT1HrMin', 'AT5minMin','T_Min', 'T Min'],
    'ATMax' : ['AT1HrMax','AT5minMax', 'T_Max', 'T Max'],
 
 # Relative Humidity
    'RHAvg' : ['Humedad','RH5minAvg','RHAvg','RelHumidAvg', 'Humedad R', 'RH5m2015'],
    'RHMin' : ['H_Min','RH5minMin','RelHumidMin','H_M Min'],
    'RHMax' : ['H_Max', 'RH5minMax', 'RelHumidMax','H_R Max'],

 # Wind Speed
    'WSAvg' : ['Velocidad','WS5minAvg','WSAvg','WindMnSpdSclr','WindMnSpdS'],
    'WSMin' : ['WindMinSpdSclr','WS5minMin'],
    'WSMax' : ['WindMaxSpdSclr','WS5minMax'],

 # Wind Direction
    'WDAvg' : ['Direccion', 'WDAvg','WD5minAvg','WindMnDirUnit','Dirección'],
    'WDMin' : ['WD5minMin'],
    'WDMax' : ['WD5minMax','WindMaxDir'],

 # Rain
    'PAvg' : ['Precipitacion','TB1hrAcc','TB1minAcc','TB5minAcc','Precipitación']
}

var_list = ['ATAvg','ATMin','ATMax','RHAvg','RHMin','RHMax', 'WSAvg','WSMin','WSMax','WDAvg','WDMin', 'WDMax','PAvg']
#sorted(var_list)


# In[76]:


df = read_meteo_csv(path =path,folder = 0,file = files_by_date[0])
df2 = reformat_df(df=df, replace_values=replace_values)
df2.dtypes


# In[77]:


len(files_by_date)


# ## Process files in loop

# In[18]:


get_ipython().run_line_magic('run', 'Meteo_utils.ipynb')


# In[322]:


## Variable names:
# BAT  is  battery
# Not very clear: 'H_M Min','WindMnSpdSclr','WindMnSpdS','WindMnDirUnit'
replace_values ={
# Temperature
    'ATAvg' :['AT1HrAvg', 'AT5minAvg', 'ATAvg','Temperatura','Temperatuta','TEMPERATURA AIRE Â°C PROM'],
    'ATMin' : ['AT1HrMin', 'AT5minMin','T_Min', 'T Min','TEMPERATURA AIRE Â°C MIN'],
    'ATMax' : ['AT1HrMax','AT5minMax', 'T_Max', 'T Max','TEMPERATURA AIRE Â°C MAX'],
 
 # Relative Humidity
    'RHAvg' : ['Humedad','RH5minAvg','RHAvg','RelHumidAvg', 'Humedad R', 'RH5m2015','HUMEDAD RELATIVA DEL AIRE % PROM'],
    'RHMin' : ['H_Min','RH5minMin','RelHumidMin','H_M Min','HUMEDAD RELATIVA DEL AIRE % MIN'],
    'RHMax' : ['H_Max', 'RH5minMax', 'RelHumidMax','H_R Max','HUMEDAD RELATIVA DEL AIRE % MAX'],

 # Wind Speed
    'WSAvg' : ['Velocidad','WS5minAvg','WSAvg','WindMnSpdSclr','WindMnSpdS','VIENTO VELOCIDAD m/s INST'],
    'WSMin' : ['WindMinSpdSclr','WS5minMin'],
    'WSMax' : ['WindMaxSpdSclr','WS5minMax'],

 # Wind Direction
    'WDAvg' : ['Direccion', 'WDAvg','WD5minAvg','WindMnDirUnit','Dirección','VIENTO DIRECCION Â° INST'],
    'WDMin' : ['WD5minMin'],
    'WDMax' : ['WD5minMax','WindMaxDir'],

 # Rain
    'PAvg' : ['Precipitacion','TB1hrAcc','TB1minAcc','TB5minAcc','Precipitación','PRECIPITACION mm SUM']
}

var_list = ['ATAvg','ATMin','ATMax','RHAvg','RHMin','RHMax', 'WSAvg','WSMin','WSMax','WDAvg','WDMin', 'WDMax','PAvg']
#sorted(var_list)


# In[310]:


path = '/Users/tamarahuete/Documents/Github_repos/TFM21/data/RAW'
ziplist = glob.glob(f'{path}/*.zip')
ziplist


# In[165]:


file, folder


# In[389]:


path = '/Users/tamarahuete/Documents/Github_repos/TFM21/data'
folder = 9
files_by_date = order_meteo_zip(path=f'{path}/RAW/', folder =folder)
#get_unique_variables(files_by_date,path =f'{path}/RAW/',folder = folder)

for file in range(50, len(files_by_date)):
        print(f'{file}/{len(files_by_date)}')
        df = read_meteo_csv(path =f'{path}/RAW',folder = folder,file = files_by_date[file])    
        df2 = reformat_df(df=df, replace_values=replace_values)
        master_df = master_df.append(df2)
        
export_name = f'{files_by_date[0].split("/")[0].replace(" ","").replace(".","")}'
repeat = list(set([export_name +'.csv']) & set(os.listdir(f'{path}/PROCESSED')))
if len(repeat)>0:
    master_df.to_csv(f'{path}/PROCESSED/{export_name}_{len(repeat)+1}.csv')
else :
    master_df.to_csv(f'{path}/PROCESSED/{export_name}.csv')


# In[313]:


df


# In[380]:


files_by_date = order_meteo_zip(path=f'{path}/RAW/', folder =8,only_csv=False)
files_by_date


# In[381]:


path = '/Users/tamarahuete/Documents/Github_repos/TFM21/data'
ziplist = glob.glob(f'{path}/RAW/*.zip')
for folder in range(9, len(ziplist)):
    
    files_by_date = order_meteo_zip(path=f'{path}/RAW/', folder =folder)
    #get_unique_variables(files_by_date,path =f'{path}/RAW/',folder = folder)

    master_df =pd.DataFrame()
    for file in range(0, len(files_by_date)):
        print(f'{file}/{len(files_by_date)}')
        df = read_meteo_csv(path =f'{path}/RAW',folder = folder,file = files_by_date[file])    
        df2 = reformat_df(df=df, replace_values=replace_values)
        master_df = master_df.append(df2)
        
    export_name = f'{files_by_date[0].split("/")[0].replace(" ","").replace(".","")}'
    repeat = list(set([export_name +'.csv']) & set(os.listdir(f'{path}/PROCESSED')))
    if len(repeat)>0:
        master_df.to_csv(f'{path}/PROCESSED/{export_name}_{len(repeat)+1}.csv')
    else :
        master_df.to_csv(f'{path}/PROCESSED/{export_name}.csv')


# In[374]:


get_ipython().run_line_magic('run', 'Meteo_utils.ipynb')


# In[382]:


file, folder


# In[383]:


df = read_meteo_csv(path =f'{path}/RAW',folder = folder,file = files_by_date[file])    
#df2 = reformat_df(df=df, replace_values=replace_values)


# In[384]:


df


# In[348]:


df2 = reformat_df(df=df, replace_values=replace_values)


# In[375]:


folder =8


# In[376]:


ziplist = glob.glob(f'{path}/RAW/*.zip')
zf = zipfile.ZipFile(f'{ziplist[folder]}')


# In[299]:


if len(df.columns) == 1:
        df = df[df.columns[0]].str.split(',',expand=True)
        if len(df.columns) == 1:
            df = df[df.columns[0]].str.split('.',expand=True)
            df[3] =df[3].astype(str).str.cat(df[4].astype(str),sep=".")
            df.drop(columns=4, inplace=True)
        df = df.iloc[1:]   


# In[303]:


df

