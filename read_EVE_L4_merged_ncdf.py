# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 07:29:57 2022

@author: rodney.viereck
"""
# read_EVE_data

import pandas as pd
import netCDF4 as nc
import numpy as np
from datetime import datetime as dt
import math



ipath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/SDO_EVE/"
opath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/SDO_EVE/"
         # C:\Users\rodney.viereck\Documents\Python\EUV_2\SDO_EVE

ifile = "EVE_L4_merged_c24h_v008_2010_2024.ncdf"
# ifile = 'latest_EVE_L3_merged_1nm.ncdf'
# ifile = 'latest_EVE_L3_merged_V8.ncdf'
# ifile = 'EVE_l3_merged_1nm_V8.ncdf'
# ifile = 'EVE_L3_merged_V8.ncdf'
# ofile = 'SDO_EVE_spectra_V8.dat'
# ofile = 'SDO_EVE_spectra_1nm_V8.dat'

ofile = "EVE_L4_V8_spec_2010-2024.dat"

spec_eve = nc.Dataset(ipath+ifile)

spec_eve_items  = list(spec_eve.variables.keys())


YYYYDOY = spec_eve.variables['DATA.YYYY_DOY'][0]

dates = []

for i1 in range(len(YYYYDOY)):
    date1 = dt.strptime(str(int(YYYYDOY[i1])), '%Y%j')
    # date2 = dt(date1[0],date1[1],int(date1[2]),12)
    # print(i1,date1,date2)
    dates.append(date1)


spec_irr = np.ma.getdata(spec_eve.variables['DATA.IRRADIANCE'][0])
spec_wl = np.ma.getdata(spec_eve.variables['WAVELENGTH'][0])


mf = 5.05e11  # Planks Constant, the speed of light, and cm2 to m2

bin_per_nm = 50.

for i1 in range(len(spec_wl)):
    spec_wl[i1] = float(int(100 * spec_wl[i1]))/100.
    spec_irr[:,i1] = spec_irr[:,i1] * spec_wl[i1] * mf  / bin_per_nm    # Convert to Photons per bin                           

print('Create DataFrame')

# sp_df = pd.DataFrame(spec_irr).transpose()
sp_df = pd.DataFrame(spec_irr)

col_names = spec_wl

    
sp_df = sp_df.set_axis(col_names, axis = 1)
    
sp_df.insert(0,'Datetime',dates, True)
sp_df = sp_df.set_index('Datetime')

stop()

print("Write to file ", opath + ofile)

sp_df.to_csv(opath + ofile,float_format='%2.4e')
