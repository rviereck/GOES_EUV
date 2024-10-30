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

write_file = True
year = "2010"


ipath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/TIMED_SEE/"
opath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/combined/"

ifile = "TIMED_SEE_Spectra_2010-2024.dat"

mg_file = "C:/Users/rodney.viereck/Documents/Python/EUV/input/Bremen_MgII_Index.csv"

xrs_path = "C:/Users/rodney.viereck/Documents/Python/EUV/input/GOES/"
xrs_file = "XRS_2010-2020.dat"


# ***************************  Read Files *********

#Read SEE file

see_df = pd.read_csv(ipath + ifile)
see_df['Datetime'] = pd.to_datetime(see_df['Datetime'])
see_df = see_df.set_index('Datetime')
see_df = see_df[see_df[:] >0]
# drop_cols=[176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194]
see_df.drop(see_df.columns[176:195],axis=1,inplace=True)


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

for i1 in range (num_cols):
    see_df.iloc[:,i1] = see_df.iloc[:,i1] * (i1+0.5) * hf # i1 = wl[nm], 0.5 = wl_band_half_width


# see_df = see_df[np.invert(np.isnan(see_df[:]))]
# see_df = see_df.dropna()

#Read GOES XRS file
print("Reading GOES XRS Data")
goes_df = pd.read_csv(xrs_path + xrs_file)
goes_df['Datetime'] = pd.to_datetime(goes_df['Datetime'])
goes_df = goes_df.set_index('Datetime')
goes_df = goes_df[goes_df[:] >0]
goes_df = goes_df.dropna()

# goes_df.iloc[:,0] = goes_df.iloc[:,0] * 0.02 * mf
# goes_df.iloc[:,1] = goes_df.iloc[:,1] * 0.06 * mf

#Rename Columns
# for i1 in range (176):
#     see_df.rename(columns= {see_df.columns[i1]: str(i1)+"-"+str(i1+1)}, inplace = True)



#Read MgII file
print("Reading MgII Data")
mg_df = pd.read_csv(mg_file, sep=',')
mg_df['year'] = mg_df['fractional_year'].astype(int)
mg_df = mg_df.rename(columns={' month':'month', ' day':'day'})
mg_df['Datetime'] = pd.to_datetime(mg_df[['year', 'month', 'day']])
mg_df = mg_df.set_index('Datetime')
mg_df = mg_df[(mg_df.index>=dt(2002,1,1)) & (mg_df.index < dt(2025,1,1))]
mg_df = mg_df.drop(columns = ['fractional_year', 'month', 'day', 'year', ' uncertainty(1s)',  ' source_id'])
mg_df = mg_df[mg_df[' index'] > 0]
mg_df = mg_df.rename({' index':'Mg_index'}, axis = 1)
mg_df = mg_df.dropna()


#Combine data frames interpolating to the SEE index

see_df["Mg_index"] = np.nan
see_df["XRS_short"] = np.nan
see_df["XRS_long"] = np.nan


print("Combining GOES and MgII Data to SEE Data  (This may take a while)")
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
    
    if pd.isnull(goes_nearest) == False:  # Check for Nuls NaNs and NaTs
        see_df.at[i, 'XRS_short'] = goes_df.loc[goes_nearest]['xrs_short']
        see_df.at[i, 'XRS_long'] = goes_df.loc[goes_nearest]['xrs_long']
    i1 = i1+1

# see_df = see_df.dropna()

#Move XRS columns to the first two...

print("Rearranging DataFrame Columns")

see_df.insert(0,'xrs_long',0)
see_df.insert(0,'xrs_short',0)

see_df['xrs_long'] = see_df['XRS_long']
see_df['xrs_short'] = see_df['XRS_short']

see_df.drop('XRS_long', axis = 1, inplace=True)
see_df.drop('XRS_short', axis = 1, inplace=True)
     

#   Save csv files


ofile = 'Combined_SEE_GOES_Mg_2010-2024.dat'

print(opath + ofile)

 
see_df.to_csv(opath +ofile, float_format='%.5e')
# store['see_df'] = sp_dfo





