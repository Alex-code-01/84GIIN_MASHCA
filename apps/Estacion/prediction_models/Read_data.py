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
from . import Meteo_utils as mu
#from pyproj import Proj
#%run Meteo_utils.ipynb

def main(path):    
    folder = 0
    file = 0  
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
    df = mu.read_meteo_csv(path =path,folder = folder,file = file)
    df2 = mu.reformat_df(df=df, replace_values=replace_values)
    print(df2.dtypes)    

