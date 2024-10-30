# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 07:29:57 2022

Combines annual TIMED-SEE HDF5 with MgII.

@author: rodney.viereck
"""
# read_EVE_data

import pandas as pd
# import netCDF4 as nc
from datetime import datetime as dt
from datetime import timedelta as tdelta
# import matplotlib.pyplot as plt
import numpy as np
# import array
# import lmfit
# import scipy

write_file = False
year = "2010"


ipath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/TIMED_SEE/"
ifile = "TIMED_SEE_Spectra_2010-2024.dat"

mg_file = "C:/Users/rodney.viereck/Documents/Python/EUV/input/Bremen_MgII_Index.csv"

xrs_path = "C:/Users/rodney.viereck/Documents/Python/EUV_2/GOES/"
xrs_file = "GOES_XRS_Combined.dat"

opath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/combined/"

start_date = dt(2017,2,9)
end_date = dt(2024,10,1)

# ***************************  Read Files *********

#Read SEE file

print("Reading SEE data")

see_df = pd.read_csv(ipath + ifile)
see_df['Datetime'] = pd.to_datetime(see_df['Datetime'])
see_df = see_df.set_index('Datetime')
# see_df = see_df[see_df[:] >0]
# drop_cols=[176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194]
see_df.drop(see_df.columns[176:195],axis=1,inplace=True)

see_df = see_df[(see_df.index>=start_date) & (see_df.index < end_date)]

see_df = see_df[see_df.min(axis = 1) >= 0]
# see_df = see_df.dropna(inplace = True)



# Convert Irradiance to Photons (I[w/m2] to P[/cm2])

# c = 2.998e8    # m/s Speed of light
# h = 6.63e-34  #J.s Planks Constant
# area_conv = 10e-4 m2/cm2
# wl_conv = 1e-9 m/nm
# wl in nm

# P[phot/cm2] = 1/hf = wl/hc = (wl[nm]/hc[Jsm])*wl_conv*area_conv
#             = 5.03e11 * wl * I

hf = 5.05e11

#   E = hc/wl  =  i x wl x 5.05e15

num_cols = len(see_df.columns)
cols = see_df.columns.values

for i1 in range (num_cols):
    wl = float(cols[i1])
    see_df.iloc[:,i1] = see_df.iloc[:,i1] * wl * hf # i1 = wl[nm], 0.5 = wl_band_half_width

see_df.dropna(inplace = True)


#Read GOES XRS file

print ("Reading GOES data")

goes_df = pd.read_csv(xrs_path + xrs_file)
goes_df['Datetime'] = pd.to_datetime(goes_df['Datetime'])
goes_df = goes_df.set_index('Datetime')
goes_df = goes_df[goes_df[:] >0]
goes_df = goes_df.dropna()

#Convert xrs data to photons
goes_df.iloc[:,0] = goes_df.iloc[:,0] * 0.02 * hf
goes_df.iloc[:,1] = goes_df.iloc[:,1] * 0.06 * hf

#Rename Columns
# for i1 in range (176):
#     see_df.rename(columns= {see_df.columns[i1]: str(i1)+"-"+str(i1+1)}, inplace = True)



#Read MgII file

print("Reading Mg II data")

mg_df = pd.read_csv(mg_file, sep=',')
mg_df['year'] = mg_df['fractional_year'].astype(int)
mg_df = mg_df.rename(columns={' month':'month', ' day':'day'})
mg_df['Datetime'] = pd.to_datetime(mg_df[['year', 'month', 'day']])
mg_df = mg_df.set_index('Datetime')
mg_df = mg_df[(mg_df.index>=start_date) & (mg_df.index < end_date)]
mg_df = mg_df.drop(columns = ['fractional_year', 'month', 'day', 'year', ' uncertainty(1s)',  ' source_id'])
mg_df = mg_df[mg_df[' index'] > 0]
mg_df = mg_df.rename({' index':'Mg_index'}, axis = 1)
mg_df.dropna(inplace = True)


#Combine data frames interpolating to the SEE index

print ("Combining Data")

see_df["Mg_index"] = np.nan
see_df["XRS_short"] = np.nan
see_df["XRS_long"] = np.nan

i1 = 0
for i in see_df.index.values:
    # print(i1,i)
    
    its = pd.Timestamp(i)
    # if its not in mg_df.loc[its]:
    mg_df.loc[i] = np.nan
        
    mg_df = mg_df.sort_index().interpolate(method='time')
    see_df.at[i,'Mg_index'] = mg_df.loc[i]['Mg_index'] 
    
    its = pd.Timestamp(i)
    goes_nearest = goes_df.index.asof(its + tdelta(seconds = 30))
    
    if pd.isnull(goes_nearest) != True:
    
        see_df.at[i, 'XRS_short'] = goes_df.loc[goes_nearest]['xrs_short']
        see_df.at[i, 'XRS_long'] = goes_df.loc[goes_nearest]['xrs_long']
        i1 = i1+1

# see_df = see_df.dropna()

#Move XRS columns to the first two...

xrs1 = see_df.pop('XRS_long')
xrs2 = see_df.pop('XRS_short')

see_df.insert(0,'xrs_long',xrs1)
see_df.insert(0,'xrs_short',xrs2)


#   Save Data to file

ofile = 'Combined_SEE_GOES_Mg_2017-2024.dat'

print("Writing to ",opath + ofile)

 
see_df.to_csv(opath +ofile, float_format='%.5e')
# store['see_df'] = sp_dfo





