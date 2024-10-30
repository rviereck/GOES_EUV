# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 07:29:57 2022

Reads TIMED-SEE NetCDF files and extracts time series of emission bands.

@author: rodney.viereck
"""
# read_EVE_data

import pandas as pd
import netCDF4 as nc
from datetime import datetime as dt
from datetime import timedelta as tdelta
import matplotlib.pyplot as plt
import numpy as np
import re

ipath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/TIMED_SEE/"
opath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/TIMED_SEE/"

# url = "https://lasp.colorado.edu/data/timed_see/level2a_xps/2009/"

ifile = 'latest_see_L3A_merged.ncdf'
ofile = 'TIMED_SEE_spectra_2001-2024.dat'

# ***************************

start_date = dt(2001, 1, 1, 0, 0)
end_date = dt(2025, 1, 1, 0, 0,)

output_daily = True

#  Create GOES Bands
goes_lines = True
five_nm = False



spec_see = nc.Dataset(ipath+ifile)

spec_see_items  = list(spec_see.variables.keys())


YYYYDOY = spec_see.variables['DATE']
SOD = spec_see.variables['TIME']
 
datetimes = []

numpts = len(YYYYDOY[0,:])
# numpts = 10

for i1 in range(numpts):
    date = dt.strptime(str(YYYYDOY[0,i1]), '%Y%j')
    date_time = date + tdelta(seconds = int(SOD[0][i1]))
    datetimes.append(date_time)
    
dt_df = pd.DataFrame(datetimes)

dt_df.columns = ['Datetime']
    

spec_irr = spec_see.variables['SP_FLUX'][0,0:numpts,:]

au_cor = spec_see.variables['COR_1AU']

for i1 in range(195):
    spec_irr[:,i1] = spec_irr[:,i1] * au_cor[0,:]    #Remove 1 AU correction

sp_df = pd.DataFrame(spec_irr)

col_names = []

for i2 in range(195):
    # col_names.append(str(i2 + 5))
    # col_names.append(str(spec_see.variables['SP_WAVE'][0][i2]))
    cn = re.findall(r"[-+]?(?:\d*\.*\d+)",str(spec_see.variables['SP_WAVE'][0][i2]))
    cn = ''.join(cn)
    col_names.append(cn)

sp_df.columns = col_names

sp_df = pd.concat([dt_df, sp_df], axis=1)

sp_df = sp_df.set_index('Datetime')

sp_df.to_csv(opath + ofile, float_format = '%.4e')

    



