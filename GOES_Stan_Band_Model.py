# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 05:44:15 2024

@author: rodney.viereck
"""

import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

ipath_goes = 'C:/Users/rodney.viereck/Documents/Python/EUV_2/GOES/'
ifile_goes = 'GOES_XRS_EUVS_Combined.dat'

ipath_coef = 'C:/Users/rodney.viereck/Documents/Python/EUV_2/stan_bands/'
ifile_coef = "GOES_StanBand_Coefficients_2.dat"

plot_spectra = False
save_file = True

print("Reading GOES XRS_EUVS file")
goes_df = pd.read_csv(ipath_goes + ifile_goes)
goes_df['Datetime'] = pd.to_datetime(goes_df['Datetime'])
goes_df.set_index('Datetime', inplace = True)


print("Reading Stan_Band Model parameter file")
coef_df = pd.read_csv(ipath_coef + ifile_coef)
coef_df.set_index('inputs', inplace = True)

#Create Stan Bands
sb_df = goes_df[["xrs_short","xrs_long"]].copy()
sb_df.rename(columns = {'xrs_short':'0.1-0.4','xrs_long':'0.4-0.8'}, inplace=True)

goes_cols = goes_df.columns
coef_names = coef_df.index
sb_columns = coef_df.columns

print ("Creating Stan Bands")
for i1 in range (2,37):
    # print(i1,sb_columns[i1])
    mod_mult = coef_df[sb_columns[i1]].values[0:10]
    constant = coef_df.loc["constant"].values
    # print(goes_cols,mod_mult)
    sb = 0
    for i2 in range (10): 
        sb = sb + goes_df[goes_cols[i2]] * mod_mult[i2]
    sb_df[sb_columns[i1]] = sb + constant[i1]
    # stop()
    # input("Hit Enter  ")
    
#Plot Spectra

if plot_spectra:

    str_date = dt.datetime(2020, 8, 8)
    end_date = dt.datetime(2020, 8, 9)
    
    sb_spec = sb_df.loc[(sb_df.index >= str_date)
                         & (sb_df.index < end_date)].mean(axis=0)
    
    sb_columns = sb_df.columns
    
    # eve_spec = eve_sb_df.loc[(eve_sb_df.index >= str_date)
    #                      & (eve_sb_df.index < end_date)].mean(axis=0)


    # f10_sb_df = f10_sb_df[(f10_sb_df.index > str_date) 
    #                       & (f10_sb_df.index <= end_date)].mean(axis=0)
    
    #Create plotting seies

    plt_spec_wl = np.zeros([(2*37)])
    plt_spec = np.zeros([(2*37)])
    # plt_f10_spec = np.zeros([(2*37)])
    # plt_see_spec = np.zeros([(2*37)])
    # plt_eve_spec = np.zeros([(2*37)])
    # plt_goes_spec = np.zeros([(2*37)])
    
    
    
    for i1 in range (37):
        if (i1 >= 11) & (i1 <= 18):
            t1 = (sb_columns[i1].split("_")[0])
            plt_spec_wl[2*i1] = float(t1.split("-")[0])
            plt_spec_wl[2*i1+1] = float(t1.split("-")[1])
            print(i1,t1,plt_spec_wl[2*i1])
        else:
            plt_spec_wl[2*i1] = float(sb_columns[i1].split("-")[0])
            plt_spec_wl[2*i1+1] = float(sb_columns[i1].split("-")[1])
            
        plt_spec[2*i1] = sb_spec.iloc[i1]
        plt_spec[2*i1+1] = sb_spec.iloc[i1]
        
        # plt_eve_spec[2*i1] = eve_spec.iloc[i1] * ymult_eve
        # plt_eve_spec[2*i1+1] = eve_spec.iloc[i1]* ymult_eve
        
        # plt_f10_spec[2*i1] = f10_sb_df.iloc[i1]
        # plt_f10_spec[2*i1+1] = f10_sb_df.iloc[i1]
        
    fig, ax1 = plt.subplots()
    
    ax1.set_title("Stan-Band Spectrum  " + str(str_date))

    ax1.plot(plt_spec_wl,plt_spec,color='red', label = "Stan_Band Spectrum")
    # ax1.plot(plt_spec_wl,plt_see_spec,color='blue', label = "SEE Spectrum")
    # ax1.plot(plt_spec_wl,plt_eve_spec,color='green', label = "EVE Spectrum")
    # ax1.plot(plt_spec_wl,plt_f10_spec,color='red', label = "WAM F10 Spec")

    ax1.set_ylim(1e8,1e12) 
    # ax1.set_xlim(60,130)
    ax1.set_yscale('log')
    ax1.legend(loc = 'lower right')
    
if save_file:
    ofile = "GOES_Stan_Bands.dat"        
    print("Writing to ", ipath_coef + ofile)    
    sb_df.to_csv(ipath_coef +ofile, float_format='%.3e')
