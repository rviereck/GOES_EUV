# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 04:07:59 2024

@author: rodney.viereck
"""
#Combine GOES XRS Data

import pandas as pd
import datetime as dt

# import numpy as np

ipath = 'C:/Users/rodney.viereck/Documents/Python/EUV_2/GOES/'

start_date = dt.datetime(2020,1,1)
end_date = dt.datetime(2021,1,1)

ifile_xrs = "GOES_XRS_combined.dat"
ifile_euvs = "GOES_EUVS_2017-2024.dat"

mf = 5.05e11  # Planks Constant, the speed of light, and cm2 to m2

print("Reading GOES XRS file")
goes_xrs_df = pd.read_csv(ipath + "xrs/" + ifile_xrs)
goes_xrs_df['Datetime'] = pd.to_datetime(goes_xrs_df['Datetime'])
goes_xrs_df.set_index('Datetime', inplace = True)
goes_xrs_df = goes_xrs_df[(goes_xrs_df.index > start_date) & (goes_xrs_df.index < end_date)]


print("Reading GOES EUVS file")
goes_euvs_df = pd.read_csv(ipath + "euvs/" + ifile_euvs)
goes_euvs_df['Datetime'] = pd.to_datetime(goes_euvs_df['Datetime'])
goes_euvs_df.set_index('Datetime', inplace = True)
goes_euvs_df = goes_euvs_df[(goes_euvs_df.index > start_date) & (goes_euvs_df.index < end_date)]

#Convert to Photons/cm2/sec
goes_xrs_df["xrs_short"] = goes_xrs_df["xrs_short"] * 0.3 * mf
goes_xrs_df["xrs_long"] = goes_xrs_df["xrs_long"] * 0.6 * mf


goes_euvs_df.insert(0, "xrs_short", goes_xrs_df["xrs_short"])
goes_euvs_df.insert(1, "xrs_long", goes_xrs_df["xrs_long"])
goes_euvs_df.drop(["data_source"],axis = 1, inplace = True)

#  Remove unfilled rows
goes_euvs_df.dropna(inplace = True)

ofile = 'GOES_XRS_EUVS_Combined.dat'

print("Writing to ",ipath + ofile)

 
goes_euvs_df.to_csv(ipath +ofile, float_format='%.4e')
