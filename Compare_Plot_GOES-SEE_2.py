# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 06:51:53 2024

@author: rodney.viereck
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from PIL import Image
import datetime as dt
from datetime import timedelta as tdelta

# from scipy.ndimage.filters import uniform_filter1d

# def untuple(x):
#     return x

ipath_see = "C:/Users/rodney.viereck/Documents/Python/EUV_2/stan_bands/"
# ipath_goes = "C:/Users/rodney.viereck/Documents/Python/GOES/input/NCEI_Files/euvs/"
ipath_goes = "C:/Users/rodney.viereck/Documents/Python/EUV_2/GOES/euvs/"
opath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/combine/"
# ifile = "NRL_Spec.csv"

ifile_see = 'SEE_GOES_Mg_Stan_Bands_2010-2024.dat'
# ifile_see = 'SEE_GOES_Mg_Stan_Bands_2010-2024.dat'
# ifile_eve_sb = 'EVE_StanBands_2010_2020.dat'
# ifile_goes_16 = "GOES_16_EUVS.dat"
# ifile_goes_17 = "GOES_17_EUVS.dat"
# ifile_goes_18 = "GOES_18_EUVS.dat"
ifile_goes = "GOES_EUVS_2017-2024.dat"

ofile_sb = "New_SEE_GOES_Mg_Stan_Bands_2010-2024.dat"


write_file = False
plot_spec = False
plot_ts = True
scatter_plot = True

if scatter_plot: plot_ts=True  #Need to calculate Time Series to create scatter plots


#Load See Stand Bands

see_sb_df = pd.read_csv(ipath_see+ifile_see)
see_sb_df['Datetime'] = pd.to_datetime(see_sb_df['Datetime'])
see_sb_df.set_index('Datetime', inplace = True)
see_columns = see_sb_df.columns

#Load GOES EUVS Lines

g_euv_df = pd.read_csv(ipath_goes+ifile_goes)
g_euv_df['Datetime'] = pd.to_datetime(g_euv_df['Datetime'])
g_euv_df.set_index('Datetime', inplace = True)
goes_columns = g_euv_df.columns


    
#load F10 F10 SBs

# f10_path = "C:/Users/rodney.viereck/Documents/Python/EUV/input/WAM_F10/"
# f10_sb_file = "WAM_F10_Stan_Bands_2010-2020.dat"

# f10_sb_df = pd.read_csv(f10_path + f10_sb_file)
# f10_sb_df['Datetime'] = pd.to_datetime(f10_sb_df['Datetime'])
# f10_sb_df.set_index('Datetime', inplace = True)
# f10_cols = f10_sb_df.columns


#Plot Spectra

# if plot_spec:

#     str_date = dt.datetime(2010, 8, 8)
#     end_date = dt.datetime(2010, 8, 12)
    
#     see_spec = see_sb_df.loc[(see_sb_df.index >= str_date)
#                          & (see_sb_df.index < end_date)].mean(axis=0)
    
#     # eve_spec = eve_sb_df.loc[(eve_sb_df.index >= str_date)
#     #                      & (eve_sb_df.index < end_date)].mean(axis=0)


#     # f10_sb_df = f10_sb_df[(f10_sb_df.index > str_date) 
#     #                       & (f10_sb_df.index <= end_date)].mean(axis=0)
    
#     #Create plotting seies

#     plt_spec_wl = np.zeros([(2*37)])
#     plt_f10_spec = np.zeros([(2*37)])
#     plt_see_spec = np.zeros([(2*37)])
#     plt_eve_spec = np.zeros([(2*37)])
    
    
#     ymult_see = 1#1e-4
#     ymult_eve = 1
    
    
#     for i1 in range (37):
#         plt_spec_wl[2*i1] = float(see_columns[i1].split("-")[0])
#         plt_spec_wl[2*i1+1] = float(see_columns[i1].split("-")[1])
        
#         plt_see_spec[2*i1] = see_spec.iloc[i1] * ymult_see
#         plt_see_spec[2*i1+1] = see_spec.iloc[i1]* ymult_see
        
#         # plt_eve_spec[2*i1] = eve_spec.iloc[i1] * ymult_eve
#         # plt_eve_spec[2*i1+1] = eve_spec.iloc[i1]* ymult_eve
        
#         # plt_f10_spec[2*i1] = f10_sb_df.iloc[i1]
#         # plt_f10_spec[2*i1+1] = f10_sb_df.iloc[i1]
        
#     fig, ax1 = plt.subplots()
    
#     ax1.set_title("Stan-Band Spectrum  " + str(str_date))

#     ax1.plot(plt_spec_wl,plt_see_spec,color='blue', label = "SEE Spectrum")
#     ax1.plot(plt_spec_wl,plt_eve_spec,color='green', label = "EVE Spectrum")
#     ax1.plot(plt_spec_wl,plt_f10_spec,color='red', label = "WAM F10 Spec")

#     # ax1.set_ylim(1e8,1e12) 
#     # ax1.set_xlim(60,130)
#     ax1.set_yscale('log')
#     ax1.legend(loc = 'upper left')
    
if plot_ts:
    
    # sb_to_plot = 
    goes_line_to_plot = 3
    
    sb_to_plot = goes_line_to_plot+39

    
    ymin1 = 0
    ymax1 = 5e9
    
    ymin2 = 0
    ymax2 = 5
    
    ymult_eve = 1. 
    ymult_see = 1.   
    ymult_f10 = 1.
    
    str_date = dt.datetime(2018,6,1)
    end_date = dt.datetime(2024,9,1)
    
    # see_col = see_sb_df.columns
    # goes_col = goes_16_df.columns
    

    # for line_num in range (7):
    # goes_line_to_plot = line_num
    # sb_to_plot = line_num + 39
    
    # see_col_to_plot = see_col[sb_to_plot]
    # goes_col_to_plot = goes_16_df.columns[goes_line_to_plot]
    
    print("Adding ")
    
    # eve_ts = eve_sb_df[eve_col_to_plot].loc[(eve_sb_df.index >= str_date)
    #                      & (eve_sb_df.index < end_date)] * ymult_eve
    
    see_ts_df = see_sb_df[see_sb_df.columns[39:47]][(see_sb_df.index >= str_date)
                          & (see_sb_df.index < end_date)]
    see_sb_df2 = see_sb_df[see_sb_df.columns[:]][(see_sb_df.index >= str_date)
                          & (see_sb_df.index < end_date)]
    for i1 in range(8):
        see_ts_df.rename(columns={see_ts_df.columns[i1]:see_ts_df.columns[i1]+"_see"},inplace = True)

    
    
    
    # if scatter_plot == False:
    #     # fig, ax1 = plt.subplots()
    #     # ax1.plot(see_ts,color = 'red', label = 'SEE Time Series')   
    #     # ax1.plot(goes_16_ts, color = 'blue', label = 'GOES 16 Time Series')
    #     # ax1.plot(goes_17_ts, color = 'green', label = 'GOES 17 Time Series')
    #     # ax1.plot(goes_18_ts, color = 'purple', label = 'GOES 18 Time Series')
    
    
    #     # # ax1.plot(goes_ts,color = 'red', label = 'F10 Time Series')
        
    #     # ax1.set_title("GOES Line " + goes_col_to_plot)
        
    
        
        
    #     # ax1.set_ylim(ymin1,ymax1) 
        
    #     # ax2 = ax1.twinx()
            
           
    #     # ax2.plot(both_df["ratio1"],label = "Ratio SEE/EVE", color = "black",lw = 1 )
    #     # ax2.plot(both_df["ratio2"],label = "Ratio SEE/F10", color = "grey",lw = 1 )
    #     # ax2.axhline(1, color = 'k', lw = .5)
    #     # ax2.set_xlim(xmin,xmax)
    
    #     # ax2.set_ylim(ymin2,ymax2) 
        
    #     # ax1.legend(loc = "upper left")
    #     # ax2.legend(loc = "upper right")
        

    
    #     plt.show()
    
if scatter_plot:
    
    print("Resampling Data for Scatter Plots")
    
    new_cols = []
    
    for i1 in range(8):
        goes_col = g_euv_df.columns[i1]
        new_cols.append(see_ts_df.columns[i1].replace("see", "goes"))
        see_ts_df[new_cols[i1]] = np.nan
        
        
    for i4 in range(8):
        g_euv_df.rename(columns = {g_euv_df.columns[i4]:new_cols[i4]}, inplace = True)
        

    i1 = 0
    for i in see_ts_df.index.values:
    
        its = pd.Timestamp(i)
        goes_nearest = g_euv_df.index.asof(its + tdelta(seconds = 30))
        
        if pd.isnull(goes_nearest) == False:  # Check for Nuls NaNs and NaTs
            for i3 in range(8):
                see_ts_df.at[i, new_cols[i3]] = g_euv_df.loc[goes_nearest][g_euv_df.columns[i3]]

    #   Save csv files


    # ofile = 'GOES_lines_2018-2024.dat'
    # print(opath + ofile)     
    # see_ts_df.to_csv(opath +ofile, float_format='%.5e')
    
    
    fig, ax1 = plt.subplots()
    
    c1 = see_ts_df.columns
    
    col = 0
    ax1.scatter(see_ts_df[c1[col]],see_ts_df[c1[col + 7]],s=.1)
    
    # lim1 = 4e9•
    
    
    plt.show()
    
    print("Adding GOES goes_lines to the see Stan-Band file")

    
    g_cols = see_ts_df.columns[8:16]
    
    for icol in range (len(g_cols)):
        see_sb_df2[g_cols[icol]] = see_ts_df[g_cols[icol]]
    
    print('Saving new Stan_Band file to ', ipath_see+ofile_sb)
    
    see_sb_df2.to_csv(ipath_see+ofile_sb, float_format='%.5e')
    
