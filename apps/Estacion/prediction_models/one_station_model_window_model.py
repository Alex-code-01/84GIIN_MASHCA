import os
import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
#from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import math
#from scipy import stats
import json


def main(path):
    ## sampling frequency
    sample_freq = 60 #(time in minutes)
    steps=int(sample_freq/5)    
    df = pd.read_csv(path)
    df.head()
    #### The data has already been cleaned, wind transformed to vector and added perodicity
    ### Check for NAN values and delete before running models
    df.isna().sum()
    df.isnull().values.any()
    ### Subsample to get data for every hour (starting from index 0, get 12 steps)
    df = df[0::steps]
    df.head()
    date_time = pd.to_datetime(df.pop('Date_Time'), format='%Y-%m-%d %H:%M:%S')

    plot_cols = ['ATAvg', 'RHAvg', 'WAvgx','WAvgy']
    plot_features = df[plot_cols]
    plot_features.index = date_time
    _ = plot_features.plot(subplots=True)

    plot_features = df[plot_cols][:480]
    plot_features.index = date_time[:480]
    _ = plot_features.plot(subplots=True)

    df.describe().transpose()

    ### Remove PAvg and WMaxx, WMiny, WDAvg and WSAvg
    df = df[['ATAvg','ATMax','ATMin',
             'RHAvg','RHMin','RHMax',
            'WAvgx','WAvgy', 'WMinx', 'WMiny',
            'Day_sin', 'Day_cos', 'Year_sin', 'Year_cos']]

    
    ### Split data into 70%, 20%, 10% split for the training, validation, and test sets
    column_indices = {name: i for i, name in enumerate(df.columns)}

    n = len(df)
    train_df = df[0:int(n*0.7)]
    val_df = df[int(n*0.7):int(n*0.9)]
    test_df = df[int(n*0.9):]

    num_features = df.shape[1]

    ### Normalize the data  ### ROOM TO MAKE TESTS (this is just an average)
    train_mean = train_df.mean()
    train_std = train_df.std()

    train_df = (train_df - train_mean) / train_std
    val_df = (val_df - train_mean) / train_std
    test_df = (test_df - train_mean) / train_std

    ## Feature distributions
    df_std = (df - train_mean) / train_std
    df_std = df_std.melt(var_name='Column', value_name='Normalized')
    plt.figure(figsize=(12, 6))
    ax = sns.violinplot(x='Column', y='Normalized', data=df_std)
    _ = ax.set_xticklabels(df.keys(), rotation=90)
    