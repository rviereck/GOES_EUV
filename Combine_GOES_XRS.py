# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 04:07:59 2024

@author: rodney.viereck
"""
#Combine GOES XRS Data

import pandas as pd
import numpy as np

ipath = 'C:/Users/rodney.viereck/Documents/Python/EUV_2/GOES/'

ifile_16 = "GOES_16_XRS_2017-2024.dat" 
ifile_17 = "GOES_17_XRS_2018-2023.dat"
ifile_18 = "GOES_18_XRS_2022-2024.dat"

xrs_df = pd.DataFrame(pd.date_range(start = '2017-02-08 00:00:00', 
                           end = '2024-10-01 00:00:00',
                           freq='min'), 
                           columns = ['Datetime'])
xrs_df = xrs_df.set_index('Datetime')
xrs_df['xrs_long'] = np.nan
xrs_df['xrs_short'] = np.nan
xrs_df['data_source'] = np.nan


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

print('Copy GOES 16 Data')

xrs_df['xrs_long'] = g16_df['xrs_long']
xrs_df['xrs_short'] = g16_df['xrs_short']
xrs_df['data_source'] = g16_df['data_source']

print("Fill gaps with GOES 17 Data")
xrs_df.fillna(g17_df, inplace = True)

print("Fill gaps with GOES 18 Data")
xrs_df.fillna(g18_df, inplace = True)

#  Remove unfilled rows
xrs_df.dropna(inplace = True)

ofile = 'GOES_XRS_Combined.dat'

print("Writing to ",ipath + ofile)

 
xrs_df.to_csv(ipath +ofile, float_format='%.5e')
