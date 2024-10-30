# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 06:51:53 2024

@author: rodney.viereck
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from PIL import Image
from datetime import datetime as dt
from datetime import timedelta as tdelta

# from scipy.ndimage.filters import uniform_filter1d

write_file = True
plot_data = False
plot_spec = False

# ipath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/TIMED_SEE/"
opath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/stan_bands/"


# f10_path = "C:/Users/rodney.viereck/Documents/Python/EUV/input/WAM_F10/"
# f10_sb_file = "WAM_F10_Stan_Bands_2010-2020.dat"

ipath_see = "C:/Users/rodney.viereck/Documents/Python/EUV_2/combined/"
ifile_see = 'Combined_SEE_GOES_Mg_2017-2024.dat'

ipath_goes = "C:/Users/rodney.viereck/Documents/Python/EUV_2/GOES/euvs/"
ifile_goes = "GOES_EUVS_2017-2024.dat"

# eve_path = "C:/Users/rodney.viereck/Documents/Python/EUV/output/"
# eve_file = "SDO_EVE_spectra_V8.dat"

ofile = "SEE_GOES_Mg_Stan_Bands_2017-2024.dat"
# ofile_eve = "EVE_StanBands_2010_2020.dat"

str_date = dt(2018,6,1)
end_date = dt(2024,9,1)

Stan_Bands = np.array([[0.1,0.4],[0.4,0.8],[0.8,1.8],[1.8,3.2],[3.2,7.0],[7.0,15.5],[15.5,22.4],\
      [22.4,29.0],[29.0,32.0],[32.0,54.0],[54.0,65.0],[65.0,79.7],[65.0,79.7],[79.7,91.3],\
      [79.7,91.3],[79.7,91.3],[91.3,97.5],[91.3,97.5],[91.3,97.5],[97.5,98.7],[98.7,102.7],\
      [102.7,105.],[105.,110.],[110.,115.],[115.,120.],[120.,121.5],[121.5,125.],[125.,130.],\
      [130.,135.],[135.,140.],[140.,145.],[145.,150.],[150.,155.],[155.,160.],[160.,165.],\
      [165.,170.],[170.,175.]])  #Note  120 nm band had to be widdened to capture Ly alpha from low_res spectra

goes_lines = np.array([25.6,28.4,30.4,117.5,121.6,133.5,140.5])

    # Set multipliers for fixed ratios in overlapping Stan Bands

ymult = np.zeros(37)
ymult.fill(1.)
ymult[11] = 0.55  # for 65.0 nm band
ymult[12] = 0.45
ymult[13] = 0.3  # for 79.9 nm band
ymult[14] = 0.6
ymult[15] = 0.1
ymult[16] = 0.18  # for 91.3 nm band
ymult[17] = 0.48
ymult[18] = 0.34

print("Reading TIMED SEE file")
see_df = pd.read_csv(ipath_see+ifile_see)
see_df['Datetime'] = pd.to_datetime(see_df['Datetime'])
see_df.set_index('Datetime', inplace = True)

# see_df.rename(columns = {'xrs_short': '0.3', 'xrs_long': '0.6', 'Mg_index': '280'}, inplace = True)
see_df.rename(columns = {'xrs_short': '0.2', 'xrs_long': '0.4', 'Mg_index': '280.0'}, inplace = True)
# see_df.drop(columns = "('194.5',)", axis= 1, inplace = True)

# npts = len(see_df.columns)

#Convert column headers to real numbers
# print("Create new Column Headers")
# see_wl = np.zeros(npts)
# for i1 in range (npts):
#     t_head = see_df.columns[i1]
#     wl = t_head.split("-")
#     lwl = float(wl[0])
#     hwl = float(wl[1])
#     see_wl[i1] = "{:.1f}".format((hwl + lwl)/2.)
#     # print(t_head,see_wl[i1])
# see_df.columns = see_wl


see_df = see_df[see_df.min(axis=1) >= 0]

see_df = see_df[see_df.columns[:]][(see_df.index >= str_date)
                          & (see_df.index < end_date)]
see_df.dropna(inplace = True)



# eve_df = pd.read_csv(eve_path+eve_file)
# eve_df['Datetime'] = pd.to_datetime(eve_df['Datetime'])
# eve_df.set_index('Datetime', inplace = True)
# eve_df.columns = pd.to_numeric(eve_df.columns)
# wl_eve = pd.to_numeric(eve_df.columns)

# Create Stan Bands

num_bands = 37

# Create first 2 columns of new Stan Band Dataframe from the XRS channels

wll = Stan_Bands[0,0]
wlh = Stan_Bands[0,1]
col_head = str(wll)+"-"+str(wlh)

see_sb_df = pd.DataFrame(see_df['0.2']) 
see_sb_df.rename(columns={'0.2':col_head},inplace = True)

wll = Stan_Bands[1,0]
wlh = Stan_Bands[1,1]
col_head = str(wll)+"-"+str(wlh)

see_sb_df['0.4'] = see_df['0.4']
see_sb_df.rename(columns={'0.4':col_head},inplace = True)

print ("Fill In Rest of the Bands")

wl_see = pd.to_numeric(see_df.columns)

for i1 in range(2,num_bands):
    wll = Stan_Bands[i1,0]
    wlh = Stan_Bands[i1,1]
    col_head = str(wll)+"-"+str(wlh)

    print("Band ", i1, col_head)
    if (i1 == 11 or i1 == 13 or i1 == 16):col_head = col_head + "_A"
    if (i1 == 12 or i1 == 14 or i1 == 17):col_head = col_head + "_B"
    if (i1 == 15 or i1 == 18):col_head = col_head + "_C"
    see_sb_df[col_head] = ymult[i1] * see_df[see_df.columns[(wl_see>wll)&(wl_see<=wlh)]].sum(axis=1)
    # eve_sb_df[col_head] = ymult[i1] * eve_df[eve_df.columns[(wl_eve>wll)&(wl_eve<=wlh)]].sum(axis=1)
    
#  Add GOES EXIS Lines to StanBand File
print("Add GOES Lines")
goes_see_lines = np.array([0.2, 0.4, 25.5,28.5,30.5,117.5,121.5,133.5,140.5,280.0])  #GOES Lines adjusted to nearest SEE bands

for i1 in range (2,len(goes_see_lines)):
    g_col_head = "SEE_G_"+str(goes_see_lines[i1])
    print(i1,g_col_head)
    see_sb_df[g_col_head] = see_df[str(goes_see_lines[i1])]

#Add GOES EUV Lines

print('Adding GOES XRS and EUV Data')

see_sb_df['xrs_short'] = see_sb_df['0.1-0.4']
see_sb_df['xrs_long'] = see_sb_df['0.4-0.8']

g_euv_df = pd.read_csv(ipath_goes+ifile_goes)
g_euv_df['Datetime'] = pd.to_datetime(g_euv_df['Datetime'])
g_euv_df.set_index('Datetime', inplace = True)
goes_columns = g_euv_df.columns

new_cols = g_euv_df.columns

# for i1 in range(8):
#     goes_col = g_euv_df.columns[i1]
#     new_cols.append(see_ts_df.columns[i1].replace("see", "goes"))
#     see_ts_df[new_cols[i1]] = np.nan
    
    
# for i4 in range(8):
#     g_euv_df.rename(columns = {g_euv_df.columns[i4]:new_cols[i4]}, inplace = True)
    

i1 = 0
for i in see_df.index.values:

    its = pd.Timestamp(i)
    goes_nearest = g_euv_df.index.asof(its + tdelta(seconds = 30))
    
    if pd.isnull(goes_nearest) == False:  # Check for Nuls NaNs and NaTs
        for i3 in range(8):
            see_sb_df.at[i, new_cols[i3]] = g_euv_df.loc[goes_nearest][g_euv_df.columns[i3]]



#  Write to StanBand file

if write_file:
    # ofile = "SEE_Stan_Bands_2010-2024.dat"
    print ("Writing to ",opath + ofile)
    see_sb_df.to_csv(opath + ofile,float_format='%2.4e')
    
    # ofile = "EVE_Stan_Bands_2010-2020.dat"
    # print ("Writing to ",opath + ofile_eve)
    # eve_sb_df.to_csv(opath + ofile_eve,float_format='%2.4e')


#Plot

if plot_spec:
    
    #Read F10 SBs
    # f10_sb_df = pd.read_csv(f10_path + f10_sb_file)
    # f10_sb_df['Datetime'] = pd.to_datetime(f10_sb_df['Datetime'])
    # f10_sb_df.set_index('Datetime', inplace = True)
    # f10_cols = f10_sb_df.columns

    str_date = dt(2017, 8, 8)
    end_date = dt(2024, 8, 12)
    
    see_spec = see_sb_df.loc[(see_sb_df.index >= str_date)
                         & (see_sb_df.index < end_date)].mean(axis=0)
    
    # eve_spec = eve_sb_df.loc[(eve_df.index >= str_date)
    #                      & (eve_df.index < end_date)].mean(axis=0)


    # f10_sb_df = f10_sb_df[(f10_sb_df.index > str_date) 
    #                       & (f10_sb_df.index <= end_date)].mean(axis=0)
    # sb_spec.iloc[1] = 100.
    
    
    ymult2 = 3.86e-6
    ymult2 = 1.
    
 
    ymult_see = 1e-4
    ymult_eve = 1e-1
    
    plt_spec_wl = np.zeros([(2*37)])
    plt_f10_spec = np.zeros([(2*37)])
    plt_see_spec = np.zeros([(2*37)])
    plt_eve_spec = np.zeros([(2*37)])
    
    
    for i1 in range (37):
        plt_spec_wl[2*i1] = Stan_Bands[i1,0]
        plt_spec_wl[2*i1+1] = Stan_Bands[i1,1]
        
        plt_see_spec[2*i1] = see_spec.iloc[i1] * ymult_see
        plt_see_spec[2*i1+1] = see_spec.iloc[i1]* ymult_see
        
        # plt_eve_spec[2*i1] = eve_spec.iloc[i1] * ymult_eve
        # plt_eve_spec[2*i1+1] = eve_spec.iloc[i1]* ymult_eve
        
        # plt_f10_spec[2*i1] = f10_sb_df.iloc[i1]
        # plt_f10_spec[2*i1+1] = f10_sb_df.iloc[i1]
        
    fig, ax1 = plt.subplots()
    
    ax1.set_title("SEE SB Spectrum")

    ax1.plot(plt_spec_wl,plt_see_spec,color='blue', label = "SEE Spectrum")
    ax1.plot(plt_spec_wl,plt_eve_spec,color='green', label = "EVE Spectrum")
    # ax1.plot(plt_spec_wl,plt_f10_spec,color='red', label = "WAM F10 Spec")

    ax1.set_ylim(1e8,1e12)    
    ax1.set_yscale('log')
    ax1.legend(loc = 'upper left')
    
    plt.plot()
    
    # stop()
    
        
    # ratio = plt_spec[:,1]/f10_spec
        
    # xmin = 0
    # xmax = 175
    # ymin1 = 1e5
    # ymax1 = 1e12
    # ymin2 = 0
    # ymax2 = 10
        
    # fig, ax1 = plt.subplots()
    
    # ax1.set_title("SEE SB Spectrum")

    # ax1.plot(plt_spec[:,0],plt_spec[:,1],color='red', label = str(see_sb_df.index[2955].date()))
    # ax1.plot(plt_spec[:,0],f10_spec,color='blue', label = "WAM F10 Spec")

    # ax1.set_ylim(ymin1,ymax1) 
    # ax1.set_xlim(xmin,xmax)
    # ax1.set_yscale('log')
    # ax1.legend(loc = 'upper left')
    
    # ax2 = ax1.twinx()
    


    
    # ax2.plot(plt_spec[:,0], ratio,label = "Ratio", color = "green",lw = 1 )
    # ax2.axhline(1, color = 'k', lw = .5)
    # ax2.set_xlim(xmin,xmax)
    # ax2.set_ylim(ymin2,ymax2) 
    
    # ax1.legend(loc = "upper right")
    # ax2.legend(loc = "lower right")

if plot_data:
    fig, ax1 = plt.subplots()   
    
    
    ax1.set_title("SEE Time Series")
    
    col = '22.4-29.0'
    ax1.plot(see_sb_df[col],color='red', label = "SEE "+col)
    
    col = 'GOES_28.4'
    ax1.plot(see_sb_df[col],color='blue', label = "SEE "+col)
    
    ax1.legend(loc = 'upper left')



  