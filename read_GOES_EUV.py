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

ifile = ['sci_euvs-l2-avg1m_g16_s20170207_e20240920_v1-0-5.nc',
         'sci_euvs-l2-avg1m_g17_s20180601_e20230110_v1-0-5.nc',
         'sci_euvs-l2-avg1m_g18_s20220909_e20240920_v1-0-5.nc']


out_path = 'C:/Users/rodney.viereck/Documents/Python/EUV_2/GOES/euvs/'
out_file = 'GOES_combine_EUVS.dat'

vname = ['irr_256','irr_284','irr_304','irr_1175','irr_1216','irr_1335','irr_1405','MgII_standard','irr_304_flag']
    
t0 = dt.datetime(2000, 1, 1, 12, 00)

transition_date = dt.datetime(2023,1,1)

# data = requests.get(file + '#mode=bytes').content
nc0 = ncdf.Dataset(ipath + ifile[0])
nc1 = ncdf.Dataset(ipath + ifile[1])
nc2 = ncdf.Dataset(ipath + ifile[2])

mf = 5.05e11  # Planks Constant, the speed of light, and cm2 to m2

bin_per_nm = 1.
goes_lines = np.array([25.6,28.4,30.4,117.5,121.6,133.5,140.5,280.])


#   Read in GOES 16 EUVS Data

variables = nc1.variables.keys()    
times = np.array(nc1.variables['time'])    
nvals = len(times)    
datetimes = np.array([t0 + dt.timedelta(seconds = times[i1]) for i1 in range(nvals)])
cols = np.array(nc1.variables[vname[0]])
ncols = len(vname)
h = np.zeros([ncols,nvals])
for c1 in range(ncols):
    h[c1,:] = np.array(nc1.variables[vname[c1]][:])

cols = np.transpose(h)
times2 = datetimes
cols2 = cols

goes_16_df = pd.DataFrame(cols2,index=times2)
goes_16_df.index.name = 'Datetime'
goes_16_df.columns = vname
goes_16_df.replace(-9999.0, np.nan, regex=True, inplace = True)  
goes_16_df.dropna(inplace = True)
condition = goes_16_df[(goes_16_df['irr_304_flag'] != 0)].index
goes_16_df.drop(condition, inplace = True)
goes_16_df.drop('irr_304_flag', axis =1, inplace = True)

# convert to photons

for i1 in range(7):
    goes_16_df[vname[i1]] = goes_16_df[vname[i1]] * goes_lines[i1] * mf  / bin_per_nm    # Convert to Photons per bin                           

ofile = 'GOES_16_EUVS.dat'
print(opath + ofile) 
goes_16_df.to_csv(opath +ofile, float_format='%.5e')


#   Read in GOES 17 EUVS Data

variables = nc2.variables.keys()    
times = np.array(nc2.variables['time'])    
nvals = len(times)    
datetimes = np.array([t0 + dt.timedelta(seconds = times[i1]) for i1 in range(nvals)])
cols = np.array(nc2.variables[vname[0]])
ncols = len(vname)
h = np.zeros([ncols,nvals])
for c1 in range(ncols):
    h[c1,:] = np.array(nc2.variables[vname[c1]][:])

cols = np.transpose(h)
times2 = datetimes
cols2 = cols

goes_17_df = pd.DataFrame(cols2,index=times2)
goes_17_df.index.name = 'Datetime'
goes_17_df.columns = vname
goes_17_df.replace(-9999.0, np.nan, regex=True, inplace = True)  
goes_17_df.dropna(inplace = True)
condition = goes_17_df[(goes_17_df['irr_304_flag'] != 0)].index
goes_17_df.drop(condition, inplace = True)
goes_17_df.drop('irr_304_flag', axis =1, inplace = True)

# convert to photons

for i1 in range(7):
    goes_17_df[vname[i1]] = goes_17_df[vname[i1]] * goes_lines[i1] * mf  / bin_per_nm    # Convert to Photons per bin                           


ofile = 'GOES_17_EUVS.dat'
print(opath + ofile) 
goes_17_df.to_csv(opath +ofile, float_format='%.5e')

#   Read in GOES 18 EUVS Data

variables = nc2.variables.keys()    
times = np.array(nc2.variables['time'])    
nvals = len(times)    
datetimes = np.array([t0 + dt.timedelta(seconds = times[i1]) for i1 in range(nvals)])
cols = np.array(nc2.variables[vname[0]])
ncols = len(vname)
h = np.zeros([ncols,nvals])
for c1 in range(ncols):
    h[c1,:] = np.array(nc2.variables[vname[c1]][:])

cols = np.transpose(h)
times2 = datetimes
cols2 = cols

goes_18_df = pd.DataFrame(cols2,index=times2)
goes_18_df.index.name = 'Datetime'
goes_18_df.columns = vname
goes_18_df.replace(-9999.0, np.nan, regex=True, inplace = True)  
goes_18_df.dropna(inplace = True)
condition = goes_18_df[(goes_18_df['irr_304_flag'] != 0)].index
goes_18_df.drop(condition, inplace = True)
goes_18_df.drop('irr_304_flag', axis =1, inplace = True)

# convert to photons

for i1 in range(7):
    goes_18_df[vname[i1]] = goes_18_df[vname[i1]] * goes_lines[i1] * mf  / bin_per_nm    # Convert to Photons per bin                           

ofile = 'GOES_18_EUVS.dat'
print(opath + ofile) 
goes_18_df.to_csv(opath +ofile, float_format='%.5e')

#  Combine GOES Data into single file

# condition = goes_17_df[(goes_17_df.index <= transition_date)].index
# goes_17_df.drop(condition,inplace = True)

# goes_euvs_df = goes_16_df[goes_16_df.index <= transition_date]
# goes_euvs_df = pd.concat([goes_euvs_df, goes_17_df],axis = 1)

# ofile = 'GOES_EUVS.dat'
# print(opath + ofile) 
# goes_euvs_df.to_csv(opath +ofile, float_format='%.5e')

# v1 = vname[2]
   
# fig, ax1 = plt.subplots()
# # ax1.plot(goes_16_df[v1],color = 'green', label = 'GOES 16' + v1)   
# # ax1.plot(goes_17_df[v1],color = 'red', label = 'GOES 17' + v1)  

# ax1.plot(goes_euvs_df[v1])
# ax1.plot(goes_18_df[v1], color = 'red')


# ax1.set_title("Stan-Band Channel ")



# ax1.set_ylim(ymin1,ymax1) 

   
# print ('Writing  ', out_path + out_file)
# goes_df.to_csv(out_path + out_file, float_format = '%.4e')





# nc = netCDF4.Dataset(url)
# h = nc.variables[vname]
# times = nc.variables['time']
# jd = netCDF4.num2date(times[:],times.units)
# hs = pd.Series(h[:,station],index=jd)

# fig = plt.figure(figsize=(12,4))
# ax = fig.add_subplot(111)
# hs.plot(ax=ax,title='%s at %s' % (h.long_name,nc.id))
# ax.set_ylabel(h.units)