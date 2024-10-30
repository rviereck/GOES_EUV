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

write_files = True
plot_data = False
plot_spec = False

ipath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/combined/"
opath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/stan_bands/"


f10_path = "C:/Users/rodney.viereck/Documents/Python/EUV/input/WAM_F10/"
f10_sb_file = "WAM_F10_Stan_Bands_2010-2020.dat"

ifile_see = 'Combined_SEE_GOES_Mg_2010-2024.dat'

eve_path = "C:/Users/rodney.viereck/Documents/Python/EUV_2/combined/"
eve_file = "SDO_EVE_spectra_V8.dat"

ofile_see = "SEE_GOES_Mg_Stan_Bands_2010-2024.dat"
ofile_see_daily = "SEE_Stan_Bands_DA_2010-2024.dat"
ofile_eve = "EVE_StanBands_2010_2020.dat"

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


see_df = pd.read_csv(ipath+ifile_see)
see_df['Datetime'] = pd.to_datetime(see_df['Datetime'])
see_df.set_index('Datetime', inplace = True)

see_df.rename(columns = {'xrs_short': '0.1-0.4', 'xrs_long': '0.4-0.8', 'Mg_index': '279-281'}, inplace = True)
# see_df.drop(columns = "('194.5',)", axis= 1, inplace = True)

npts = len(see_df.columns)

#Convert column headers to real numbers

see_wl = np.zeros(npts)
for i1 in range (npts):
    t_head = see_df.columns[i1]
    wl = t_head.split("-")
    lwl = float(wl[0])
    hwl = float(wl[1])
    see_wl[i1] = float(int(10*(hwl + lwl)/2.))/10.    #Truncating values
    # print(t_head,see_wl[i1])
see_df.columns = see_wl
see_df.rename(columns={0.5:1.0},inplace = True)


see_df = see_df[see_df.min(axis=1) >= 0]
see_df = see_df.dropna()

eve_df = pd.read_csv(eve_path+eve_file)
eve_df['Datetime'] = pd.to_datetime(eve_df['Datetime'])
eve_df.set_index('Datetime', inplace = True)
eve_df.columns = pd.to_numeric(eve_df.columns)
wl_eve = pd.to_numeric(eve_df.columns)

# Create Stan Bands

num_bands = 37

wll = Stan_Bands[0,0]
wlh = Stan_Bands[0,1]

wl_see = pd.to_numeric(see_df.columns)

# Create first column of new Stan Band Dataframe


# see_sb_df = pd.DataFrame(see_df[wl_mult*see_df.columns[(wl>wll)&(wl<=wlh)]].sum(axis=1))
see_sb_df = pd.DataFrame(see_df.iloc[:,0]) #,wl_mult*see_df.iloc[:,1]])
col_head = str(wll)+"-"+str(wlh)
see_sb_df.rename(columns={0.2:col_head},inplace = True)
# see_sb_df[col_head] = see_df.iloc[:,1]

eve_sb_df = pd.DataFrame(eve_df.iloc[:,0]) #,wl_mult*eve_df.iloc[:,1]])
eve_sb_df.rename(columns={6.0 :col_head},inplace = True)
eve_sb_df[col_head] = 0. 



#  Fill in the rest of the Stan Bands

for i1 in range(1,num_bands):
    wll = Stan_Bands[i1,0]
    wlh = Stan_Bands[i1,1]
    col_head = str(wll)+"-"+str(wlh)

    # print(wll, wl_mult)
    # print("Band ", col_head)
    if (i1 == 11 or i1 == 13 or i1 == 16):col_head = col_head + "-A"
    if (i1 == 12 or i1 == 14 or i1 == 17):col_head = col_head + "-B"
    if (i1 == 15 or i1 == 18):col_head = col_head + "-C"
    see_sb_df[col_head] = ymult[i1] * see_df[see_df.columns[(wl_see>wll)&(wl_see<=wlh)]].sum(axis=1)
    eve_sb_df[col_head] = ymult[i1] * eve_df[eve_df.columns[(wl_eve>wll)&(wl_eve<=wlh)]].sum(axis=1)
    
#  Add GOES EXIS Lines to StanBand File

goes_see_lines = np.array([.2, .6, 25.5,28.5,30.5,117.5,121.5,133.5,140.5,280.0])  #GOES Lines adjusted to nearest SEE bands

for i1 in range (len(goes_see_lines)):
    g_col_head = "G_"+str(goes_see_lines[i1])
    see_sb_df[g_col_head] = see_df[goes_see_lines[i1]]


#  Write to StanBand file

if write_files:

    print ("Writing to ",opath + ofile_see)
    see_sb_df.to_csv(opath + ofile_see,float_format='%2.4e')
    

    see_sb_da_df = see_sb_df.resample('D').mean()
    print("Writing Daily to ", opath+ofile_see_daily)
    see_sb_da_df.to_csv(opath+ ofile_see_daily,float_format='%2.4e')
    
    ofile = "EVE_Stan_Bands_2010-2020.dat"
    print ("Writing to ",opath + ofile_eve)
    eve_sb_df.to_csv(opath + ofile_eve,float_format='%2.4e')


#Plot

if plot_spec:
    
    #Read F10 SBs
    f10_sb_df = pd.read_csv(f10_path + f10_sb_file)
    f10_sb_df['Datetime'] = pd.to_datetime(f10_sb_df['Datetime'])
    f10_sb_df.set_index('Datetime', inplace = True)
    f10_cols = f10_sb_df.columns

    str_date = dt(2010, 8, 8)
    end_date = dt(2010, 8, 9)
    
    # see_sb_da_df = see_sb_df.resample('D').mean()
    # print("Writing Daily to ", opath+ofile_see_daily)
    # see_sb_da_df.to_csv(opath+ ofile_see_daily,float_format='%2.4e')
    
    see_spec = see_sb_da_df.loc[(see_sb_da_df.index >= str_date)
                         & (see_sb_da_df.index < end_date)].mean(axis=0)
    
    eve_spec = eve_sb_df.loc[(eve_df.index >= str_date)
                         & (eve_df.index < end_date)].mean(axis=0)


    f10_spec = f10_sb_df[(f10_sb_df.index > str_date) 
                          & (f10_sb_df.index <= end_date)].mean(axis=0)
    # sb_spec.iloc[1] = 100.
      
 
    ymult_see = 1  #e-4
    ymult_eve = 1 #3.3e-3
    
    plt_spec_wl = np.zeros([(2*37)])
    plt_f10_spec = np.zeros([(2*37)])
    plt_see_spec = np.zeros([(2*37)])
    plt_eve_spec = np.zeros([(2*37)])
    
    
    for i1 in range (37):
        plt_spec_wl[2*i1] = Stan_Bands[i1,0]
        plt_spec_wl[2*i1+1] = Stan_Bands[i1,1]
        
        plt_see_spec[2*i1] = see_spec.iloc[i1] * ymult_see
        plt_see_spec[2*i1+1] = see_spec.iloc[i1]* ymult_see
        
        plt_eve_spec[2*i1] = eve_spec.iloc[i1] * ymult_eve  # * plt_spec_wl[2*i1]
        plt_eve_spec[2*i1+1] = eve_spec.iloc[i1]* ymult_eve  # * plt_spec_wl[2*i1]
        
        plt_f10_spec[2*i1] = f10_spec.iloc[i1]
        plt_f10_spec[2*i1+1] = f10_spec.iloc[i1]
        
    fig, ax1 = plt.subplots()
    
    ax1.set_title("SEE SB Spectrum")

    ax1.plot(plt_spec_wl,plt_see_spec,color='blue', label = "SEE Spectrum")
    ax1.plot(plt_spec_wl,plt_eve_spec,color='green', label = "EVE Spectrum")
    ax1.plot(plt_spec_wl,plt_f10_spec,color='red', label = "WAM F10 Spec")

    ax1.set_ylim(1e8,1e12)    
    ax1.set_yscale('log')
    ax1.legend(loc = 'upper left')
    
    plt.plot()
    

    
        
#     ratio = plt_spec[:,1]/f10_spec
        
#     xmin = 0
#     xmax = 175
#     ymin1 = 1e5
#     ymax1 = 1e12
#     ymin2 = 0
#     ymax2 = 10
        
#     fig, ax1 = plt.subplots()
    
#     ax1.set_title("SEE SB Spectrum")

#     ax1.plot(plt_spec[:,0],plt_spec[:,1],color='red', label = str(see_sb_df.index[2955].date()))
#     ax1.plot(plt_spec[:,0],f10_spec,color='blue', label = "WAM F10 Spec")

#     ax1.set_ylim(ymin1,ymax1) 
#     ax1.set_xlim(xmin,xmax)
#     ax1.set_yscale('log')
#     ax1.legend(loc = 'upper left')
    
#     ax2 = ax1.twinx()
    


    
#     ax2.plot(plt_spec[:,0], ratio,label = "Ratio", color = "green",lw = 1 )
#     ax2.axhline(1, color = 'k', lw = .5)
#     ax2.set_xlim(xmin,xmax)
#     ax2.set_ylim(ymin2,ymax2) 
    
#     ax1.legend(loc = "upper right")
#     ax2.legend(loc = "lower right")

# if plot_data:
#     fig, ax1 = plt.subplots()   
    
    
#     ax1.set_title("SEE Time Series")
    
#     col = '22.4-29.0'
#     ax1.plot(see_sb_df[col],color='red', label = "SEE "+col)
    
#     col = 'GOES_28.4'
#     ax1.plot(see_sb_df[col],color='blue', label = "SEE "+col)
    
#     ax1.legend(loc = 'upper left')



  