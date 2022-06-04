#!/usr/bin/env python
# coding: utf-8

# ### Meteo Station Utils

# In[17]:


def order_meteo_zip(path, folder,only_csv =True):
    ### access files 
    ziplist = glob.glob(f'{path}/*.zip')
    
    ### access folder
    zf = zipfile.ZipFile(f'{ziplist[folder]}')
    
    #extract dates of each of the zipfiles from file name
    a = []
    for i in range(len(zf.namelist())):
        date_str = zf.namelist()[i].split('/')[1]
        try:
            date_date = datetime.strptime(date_str, '%Y-%m-%d')
        except:
            continue
        a.append(date_date)
        
    # get unique values
    unique_dates = list(set(a))
    # order by date
    unique_dates.sort()
    #convert back to string
    str_dates = []
    for l in range(len(unique_dates)):
        str_dates.append(unique_dates[l].strftime('%Y-%m-%d'))
        
    ## Reorder files
    files_by_date = []
    for dates in str_dates:
        if only_csv:
            r = re.compile(f'.*/{dates}/.*.csv') # only csv files
        else:
            r = re.compile(f'.*/{dates}/.*') # all files (including excel sheets)
        newlist = list(filter(r.match, zf.namelist())) 
        files_by_date.extend(newlist)
    
    if len(files_by_date)==0:
        r = re.compile(f'.*.csv') # only csv files
        files_by_date = list(filter(r.match, zf.namelist())) 
    
    return files_by_date


# In[12]:


def read_meteo_csv(path, folder, file): 
    ### access files 
    ziplist = glob.glob(f'{path}/*.zip')
    
    ### access folder
    zf = zipfile.ZipFile(f'{ziplist[folder]}')
    
    try:
        df = pd.read_csv(zf.open(file), sep = ';', encoding = 'latin-1')
        ## get unmmaned columns:
        r = re.compile('Unnamed:') # get unnamed columns
        unnamed = list(filter(r.match, df.columns))
        for col in unnamed:
            df.drop(columns = [col],inplace =True)
            
        if len(df.columns) == 1:
            df = df[df.columns[0]].str.split(',',expand=True)
            if len(df.columns) == 1:
                df = df[df.columns[0]].str.split('.',expand=True)
                df[3] =df[3].astype(str).str.cat(df[4].astype(str),sep=".")
                df.drop(columns=4, inplace=True)
            df = df.iloc[1:]
        
        if 'Station Name' in df:
            df = pd.read_csv(zf.open(file), sep = ';', encoding = 'latin-1',skiprows=1)
            for col in cols:
                df.drop(columns = [col],inplace =True)
            df.columns = ['Date_Time','Variable', 'Value']
        print('Success sep ";", latin encoding')
    except:
        try:
            df = pd.read_csv(zf.open(file),header=None, encoding = 'latin-1')
            print('Success regular csv, no header, latin encoding')
        except:
            print('Failed')
            pass
    
    ## Detect and elminate empty columns- incluiding columns with low number of values (<1% of file)
    df = df.replace('', np.nan)
    empty_cols = [col for col in df.columns if df[col].isnull().all() or round(df[col].isnull().value_counts()[0]/len(df[col]),2) < 0.01]
    if len(list(set(empty_cols) & set(['Temperatura','Humedad','Precipitacion','Direccion','Velocidad']))) <1:
        df.drop(empty_cols,
            axis=1,
            inplace=True)
    if len(df.columns)==5:
        if df.columns.isin(['Fecha','Temperatura','Humedad','Precipitacion','Direccion','Velocidad']).sum()==5:
            df = df
        else: df.columns = ['Date', 'Time','Variable', 'Value','Type']
    if len(df.columns)==2:
        df.columns = ['Fecha','PAvg']
    
    # add frequency and file name as a variable
    freq = ['1min','1MIN','5min','5MIN','1hora', '1HORA','30seg']
    try:
        df['Freq']= re.findall('|'.join(freq),file)[0].lower()
    except:
        if len(df.columns)==2:
            df['Freq']='1day'
            
    df['file_name'] = file
    print(f'file ={file}, cols = {len(df.columns)}')
    return df


# In[ ]:


### Get unique variable names
def get_unique_variables(files_by_date, path, folder):
    summary_df = pd.DataFrame(columns = ['station','filename','colnum','colnames','nrows'])
    ### access files 
    ziplist = glob.glob(f'{path}/*.zip')
    
    ### access folder
    zf = zipfile.ZipFile(f'{ziplist[folder]}')
    
    for i in range(0,len(files_by_date)):
    
        df = read_meteo_csv(path =path,folder = folder,file =files_by_date[i])
        if len(df.columns)==7:
            try:
                colname = [list(df.Variable.unique())]
            except:
                colname= [list(df.columns)]
        else:
            colname= [list(df.columns)]
        
        fill = {'station':files_by_date[i].split('/')[0].replace(" ","").replace(".",""),
            'filename':files_by_date[i],
            'colnum':len(df.columns),
            'colnames':colname,
            'nrows':len(df)}
        summary_df = summary_df.append(fill, ignore_index=True)
        
    export_name = f'{files_by_date[i].split("/")[0].replace(" ","").replace(".","")}'
    repeat = list(set(['summary_'+export_name +'.csv']) & set(os.listdir(path)))
    if len(repeat)>0:
        summary_df.to_csv(f'{path}/summary_{export_name}_{len(repeat)+1}.csv')
    else :
        summary_df.to_csv(f'{path}/summary_{export_name}.csv')
    
    all_var = []
    for i in range(0,len(summary_df)):
        file_vars= summary_df.colnames[i][0]
        not_in_list =list(set(file_vars) - set(all_var))
        all_var.extend(not_in_list) 
    all_var = sorted([str(i) for i in all_var])
    
    return all_var


# In[16]:


def reformat_df(df, replace_values):
    
    ## delete any complete empty rows
    df.dropna(inplace=True, how = 'all')
        
    ## merge date + time
    ## replace variable names
    ## convert to long format with same column names and order
   
    if df.apply(lambda row: row.astype(str).str.contains('OFICINA').any(), axis=1).sum() == 0:
    #if (('Fecha' in df) & (len(df[df['Fecha']=='OFICINA']) <0)):
    
        #1. Wide format datasets
        r = re.compile('[Ff][Ee][Cc][Hh][Aa]') # get unnamed columns
        fecha = list(filter(r.match, df.columns))
        if len(fecha) > 0:
            df['Date_Time'] = pd.to_datetime(df[fecha[0]], errors ='coerce')
            df.drop(columns =[fecha[0]],inplace =True)
            df.dropna(subset = ['Date_Time'])
            
            ### delete extra variables
            extra = ['HUMEDAD RELATIVA DEL AIRE % INST','RADIACION SOLAR GLOBAL W/mÂ² SUM', 'RADIACION SOLAR GLOBAL W/mÂ² PROM',
                     'RADIACION SOLAR GLOBAL W/mÂ² MAX','RADIACION SOLAR REFLEJADA W/mÂ² PROM','TEMPERATURA AIRE Â°C INST', ]
            for col in extra:
                if col in df:
                    df.drop(columns = [col],inplace =True)

        
            for variable in list(replace_values.keys()):
                try:
                    df = df.rename(columns={list(set(df.columns) & set(replace_values[variable]))[0]: variable})
                except:
                    continue
        
            df['Type'] = np.nan
    
        #2. Long format datasets
        else:
            if 'Date_Time' in df:
                df['Type'] = np.nan
            else: 
                df['Date_Time']= pd.to_datetime(df['Date'] + ' ' + df['Time'], errors ='coerce')
                df.drop(columns =['Date','Time'],inplace =True)
                df.dropna(subset = ['Date_Time'])
        
            for variable in list(replace_values.keys()):
                df =df.replace(to_replace =replace_values[variable], value = variable)
    
            #Convert to long format and keep all variables
            df.drop_duplicates(inplace=True)
            df = df.reset_index().drop(columns = 'index')
            freq = df.Freq.unique()[0]
            file_name = df.file_name.unique()[0]
            try:
                df2 =df.pivot(index='Date_Time', columns='Variable').reset_index()
                df = df.pivot(index='Date_Time', columns='Variable', values='Value').reset_index()
            except:
                df2 =pd.pivot_table(df,index='Date_Time', columns='Variable',aggfunc='first').reset_index()
                df =pd.pivot_table(df,index='Date_Time', columns='Variable',values = 'Value',aggfunc='first').reset_index()
            df['Freq'] = freq
            df['Type'] = df2.Type.iloc[:,0]
            df['file_name'] = file_name
    
    
        ## Add variables that are not in the df but are in the general list
        not_in_df = list(set(replace_values.keys())-set(df.columns))
        for i in not_in_df:
            df[i]=np.nan


        keep = list(replace_values.keys())+ ['Date_Time', 'Type', 'Freq','file_name']
        empty_cols = [col for col in df.columns if df[col].isnull().all() or round(df[col].isnull().value_counts()[0]/len(df[col]),2) < 0.01]
        if len(list(set(empty_cols) - set(keep))) >0:
            df.drop(list(set(empty_cols) - set(keep)),
                axis=1,
                inplace=True)
    
        ## Order columns so all dfs have the same structure
        var_order = ['Date_Time', 'Type', 'Freq','file_name']
        var_order.extend(sorted(df.loc[:,list(set(df.columns) - set(['Date_Time', 'Type', 'Freq','file_name']))]))
        df = df.reindex(var_order, axis=1)
    
        ## make sure only the accepted variables are kept
        not_good = list(set(keep) - set(df.columns))
        df.drop(not_good)
    
        ## convert any ',' decimals to '.'
        try:
            df.iloc[:,4:] = df.iloc[:,4:].astype(float)
        except:
            cols= np.where(df.dtypes[4:]=='object')[0]+4
            df.iloc[:,cols] = df.iloc[:,cols].apply(lambda x: x.str.replace(',','.')) 
            df.iloc[:,cols] = df.iloc[:,cols].apply(pd.to_numeric, errors='coerce')
    else:
        df = pd.DataFrame(columns =list(replace_values.keys())+ ['Date_Time', 'Type', 'Freq','file_name'])
        var_order = ['Date_Time', 'Type', 'Freq','file_name']
        var_order.extend(sorted(df.loc[:,list(set(df.columns) - set(['Date_Time', 'Type', 'Freq','file_name']))]))
        df = df.reindex(var_order, axis=1)
    
    return df


# In[ ]:




