# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 08:34:05 2023

@author: rodney.viereck
"""

import requests
from matplotlib import pyplot as plt
import pandas as pd
import netCDF4 as ncdf
from bs4 import BeautifulSoup
import datetime as dt
import numpy as np
import xarray as xr


#  *********  Get filename from a url  **********************

# def listFD(url, ext=''):
#     page = requests.get(url).text
#     print (page)
#     soup = BeautifulSoup(page, 'html.parser')
#     return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]


# ext = "nc"

# sat = '16'
# st_year = '2017'
# st_mnth = '02'
# int_mnth = int(st_mnth)
# num_mnths = 12 - int_mnth + 1
       
ipath = 'C:/Users/rodney.viereck/Documents/Python/GOES/input/NCEI_files/euvs/'
opath = ipath

ifile_16 = 'GOES_16_EUVS.dat'
ifile_17 = 'GOES_17_EUVS.dat'
ifile_18 = 'GOES_18_EUVS.dat'


o_path = 'C:/Users/rodney.viereck/Documents/Python/EUV_2/GOES/euvs/'
o_file = 'GOES_EUVS_2017-2024.dat'

# vname = ['irr_256','irr_284','irr_304','irr_1175','irr_1216','irr_1335','irr_1405','MgII_standard','irr_304_flag']
    
# goes_lines = np.array([25.6,28.4,30.4,117.5,121.6,133.5,140.5,280.])


#   Read in GOES 16 EUVS Data

print("Reading GOES_16 file")
g16_df = pd.read_csv(ipath + ifile_16)
g16_df['Datetime'] = pd.to_datetime(g16_df['Datetime'])
g16_df.set_index('Datetime', inplace = True)
g16_df['data_source'] = 1

print("Reading GOES_17 file")
g17_df = pd.read_csv(ipath + ifile_17)
g17_df['Datetime'] = pd.to_datetime(g17_df['Datetime'])
g17_df.set_index('Datetime', inplace = True)
g17_df['data_source'] = 2

print("Reading GOES_18 file")
g18_df = pd.read_csv(ipath + ifile_18)
g18_df['Datetime'] = pd.to_datetime(g18_df['Datetime'])
g18_df.set_index('Datetime', inplace = True)
g18_df['data_source'] = 3


print("Combine Datasets")

euv_df = pd.DataFrame(pd.date_range(start = '2018-06-01 00:00:00', 
                           end = '2024-10-01 00:00:00',
                           freq='min'), 
                           columns = ['Datetime'])
euv_df = euv_df.set_index('Datetime')

for i1 in range (len(g16_df.columns)):
    euv_df[g16_df.columns[i1]] = np.nan
    
for i2 in range (len(g16_df.columns)):
    print(i2,g16_df.columns[i2])
    euv_df[g16_df.columns[i2]] = g16_df[g16_df.columns[i2]]
    

print("Fill gaps with GOES 17 Data")
euv_df.fillna(g17_df, inplace = True)

print("Fill gaps with GOES 18 Data")
euv_df.fillna(g18_df, inplace = True)

#  Remove unfilled rows
euv_df.dropna(inplace = True)
# euv_df.drop("irr_304_flag", axis = 1, inplace = True)


print("Writing to ",o_path + o_file)

 
euv_df.to_csv(o_path +o_file, float_format='%.5e')
