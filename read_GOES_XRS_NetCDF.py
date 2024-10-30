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



#  *********  Get filename from a url  **********************

# def listFD(url, ext=''):
#     page = requests.get(url).text
#     print (page)
#     soup = BeautifulSoup(page, 'html.parser')
#     return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]


# ext = "nc"

# sat = '17'
# st_year = '2017'
# st_mnth = '02'
# int_mnth = int(st_mnth)
# num_mnths = 12 - int_mnth + 1
       
ipath = 'C:/Users/rodney.viereck/Documents/Python/EUV_2/GOES/'

# ifile = 'sci_xrsf-l2-avg1m_g16_s20170207_e20241009_v2-2-0.nc'
# ifile = "sci_xrsf-l2-avg1m_g17_s20180601_e20230110_v2-2-0.nc"
ifile = "sci_xrsf-l2-avg1m_g18_s20220902_e20241013_v2-2-0.nc"

# ifile = "g14_xrs_1m_20100101_20100131.nc"

out_path = 'C:/Users/rodney.viereck/Documents/Python/EUV/input/'
# out_file = 'GOES_XRS_' + sat + '_' + st_year  + '.dat'
ofile = 'GOES_18_XRS_2022-2024.dat'

t0 = dt.datetime(2000, 1, 1, 12, 00)
# t0 = dt.datetime (1970, 1, 1, 0, 0)

nc = ncdf.Dataset(ipath+ifile)

i1 = 0

# for name, variable in nc.variables.items():            
#     for attrname in variable.ncattrs():
#         if name == "xrsb_flag":
#             print("\n\n", "Name ",name)
#             print ("Variable ", variable)
#             print ( "Attribute for ", attrname)
#             # print("{} -- {}".format(attrname, getattr(variable, attrname)))
#         # i1 = i1+1
#         # if i1 > 30: stop()
        
# stop()

# xrs_short= np.array(nc.variables['A_AVG'])
# xrs_long = np.array(nc.variables['B_AVG'])
# times = np.ma.getdata(nc.variables['time_tag'])


xrs_short= np.array(nc.variables['xrsa_flux'])
xrs_long = np.array(nc.variables['xrsb_flux'])
xrs_flag = np.array(nc.variables['xrsb_flag'])
times = np.ma.getdata(nc.variables['time'])

print("Entering Date Loop")
datetimes = np.zeros(len(times), dtype = object)

for i1 in range(len(times)): 
    t1 = times[i1]
    datetimes[i1] = t0 + dt.timedelta(seconds = t1)
    # print(i1,t1,datetimes[i1])
    
    
print("Creating Data Frame")
# datetime = ncdf.num2date(times[:],times.units)
# xrs_df = pd.Series(xrs_short,xrs_long,index= datetimes)
xrs_df = pd.DataFrame({"Datetime": datetimes,'xrs_short':xrs_short,'xrs_long':xrs_long, 'data_flag':xrs_flag})
xrs_df.set_index('Datetime', inplace = True)

xrs_df = xrs_df[xrs_df['data_flag'] == 0.]
xrs_df = xrs_df.drop('data_flag', axis=1)


print("Writing to file")
xrs_df.to_csv(ipath + ofile,float_format='%2.4e')



# t0 = dt.datetime(2000, 1, 1, 12, 00)

# data = requests.get(ipath+ifile + '#mode=bytes').content
# nc = ncdf.Dataset('temp1',memory = data)

# variables = nc.variables.keys()

# times = np.array(nc.variables['time'])
# datetimes = []
# for i1 in range(len(times)): 
#     datetimes = np.append(datetimes, (t0 + dt.timedelta(seconds = times[i1])))

# cols = np.array(nc.variables[vname[0]])
# for c1 in range(1,len(vname)):
#     h = np.array(nc.variables[vname[c1]])
#     cols = np.vstack((cols, h))

# cols = np.transpose(cols)






# first_loop = True

# for i1 in range (int_mnth,num_mnths):
#     st_mnth = str(i1+1).zfill(2)
        
#     url = 'https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/goes'\
#         + sat+\
#         '/l2/data/euvs-l2-avg1m_science/'\
#             + st_year + '/'\
#             + st_mnth + '/'
#     # filename = 'sci_euvs-l2-avg1m_g16_d20220101_v1-0-3.nc'
    
    
#     files_in_url = listFD(url, ext)

    
    # for file in files_in_url:
        
# file = ipath+ifile
# print (file)

# data = requests.get(file + '#mode=bytes').content
# nc = ncdf.Dataset('temp1',memory = data)

# variables = nc.variables.keys()

# times = np.array(nc.variables['time'])
# datetimes = []
# for i1 in range(len(times)): 
#     datetimes = np.append(datetimes, (t0 + dt.timedelta(seconds = times[i1])))

# cols = np.array(nc.variables[vname[0]])
# for c1 in range(1,len(vname)):
#     h = np.array(nc.variables[vname[c1]])
#     cols = np.vstack((cols, h))

# cols = np.transpose(cols)


# if first_loop:
#     times2 = datetimes
#     cols2 = cols
#     first_loop = False
# else:
#     times2 = np.append(times2, datetimes)
#     cols2 = np.vstack((cols2, cols))


    
# hs = pd.DataFrame(cols2,index=times2)
# hs.index.name = 'Datetime'
# hs.columns = vname
# hs = hs.replace(-9999.0, np.nan, regex=True)        

# hs.to_csv(out_path + out_file)





# nc = netCDF4.Dataset(url)
# h = nc.variables[vname]
# times = nc.variables['time']
# jd = netCDF4.num2date(times[:],times.units)
# hs = pd.Series(h[:,station],index=jd)

# fig = plt.figure(figsize=(12,4))
# ax = fig.add_subplot(111)
# hs.plot(ax=ax,title='%s at %s' % (h.long_name,nc.id))
# ax.set_ylabel(h.units)