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

ipath = "C:/Users/rodney.viereck/Documents/Python/EUV/input/LASP/"
opath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/SDO_EVE/"

# ifile = 'latest_EVE_L3_merged_1nm.ncdf'
# ifile = 'latest_EVE_L3_merged_V8.ncdf'
# ifile = 'EVE_l3_merged_1nm_V8.ncdf'
ifile = 'EVE_L3_merged_V8.ncdf'
ofile = 'SDO_EVE_spectra_V8.dat'
# ofile = 'SDO_EVE_spectra_1nm_V8.dat'

spec_eve = nc.Dataset(ipath+ifile)

spec_eve_items  = list(spec_eve.variables.keys())


YYYYDOY = spec_eve.variables['yyyydoy']

dates = []

for i1 in range(len(YYYYDOY)):
    dates.append(dt.strptime(str(int(YYYYDOY[i1])), '%Y%j'))

spec_irr = np.ma.getdata(spec_eve.variables['sp_irradiance'])
spec_wl = np.ma.getdata(spec_eve.variables['wavelength'])

mf = 5.05e11  # Planks Constant, the speed of light, and cm2 to m2

bin_per_nm = 50.

for i1 in range(len(spec_wl)):
    spec_wl[i1] = round(spec_wl[i1],2)
    spec_irr[i1,:] = spec_irr[i1,:] * spec_wl[i1] * mf  / bin_per_nm    # Convert to Photons per bin                           
    print(i1, spec_wl[i1])

# Create DataFrame
sp_df = pd.DataFrame(spec_irr).transpose()

col_names = spec_wl

    
sp_df = sp_df.set_axis(col_names, axis = 1)
    
sp_df.insert(0,'Datetime',dates, True)
sp_df = sp_df.set_index('Datetime')

sp_df.to_csv(opath + ofile,float_format='%2.4e')

