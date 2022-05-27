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

def main():
    current = os.getcwd()
    media = "media"    
    folder = 0
    file = "estacion_M0128/8310_5min_20190416.csv"        
    path = os.path.join(current, media, file)       
    df = mu.read_meteo_csv(path =path,folder = folder,file = file)
    print(df.head())

