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

# from scipy.ndimage.filters import uniform_filter1d

# def untuple(x):
#     return x

ipath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/stan_bands/"
opath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/stan_bands/plots/"
# ifile = "NRL_Spec.csv"

ifile_see_sb = 'SEE_GOES_Mg_Stan_Bands_DA_2010-2020.dat'
# ifile_see_sb = 'SEE_Stan_Bands_2010-2020.dat'
ifile_eve_sb = 'EVE_StanBands_2010_2020.dat'

write_file = False
plot_spec = False
plot_ts = True


#Load See Stand Bands

see_sb_df = pd.read_csv(ipath+ifile_see_sb)
see_sb_df['Datetime'] = pd.to_datetime(see_sb_df['Datetime'])
see_sb_df.set_index('Datetime', inplace = True)
see_columns = see_sb_df.columns


# Load EVE Spectra

eve_sb_df = pd.read_csv(ipath+ifile_eve_sb)
eve_sb_df['Datetime'] = pd.to_datetime(eve_sb_df['Datetime'])
eve_sb_df.set_index('Datetime', inplace = True)

    
#load F10 F10 SBs

f10_path = "C:/Users/rodney.viereck/Documents/Python/EUV/input/WAM_F10/"
f10_sb_file = "WAM_F10_Stan_Bands_2010-2020.dat"

f10_sb_df = pd.read_csv(f10_path + f10_sb_file)
f10_sb_df['Datetime'] = pd.to_datetime(f10_sb_df['Datetime'])
f10_sb_df.set_index('Datetime', inplace = True)
f10_cols = f10_sb_df.columns


#Plot Spectra

if plot_spec:

    str_date = dt.datetime(2010, 8, 8)
    end_date = dt.datetime(2010, 8, 12)
    
    see_spec = see_sb_df.loc[(see_sb_df.index >= str_date)
                         & (see_sb_df.index < end_date)].mean(axis=0)
    
    eve_spec = eve_sb_df.loc[(eve_sb_df.index >= str_date)
                         & (eve_sb_df.index < end_date)].mean(axis=0)


    f10_sb_df = f10_sb_df[(f10_sb_df.index > str_date) 
                          & (f10_sb_df.index <= end_date)].mean(axis=0)
    
    #Create plotting seies

    plt_spec_wl = np.zeros([(2*37)])
    plt_f10_spec = np.zeros([(2*37)])
    plt_see_spec = np.zeros([(2*37)])
    plt_eve_spec = np.zeros([(2*37)])
    
    
    ymult_see = 1#1e-4
    ymult_eve = 1
    
    
    for i1 in range (37):
        plt_spec_wl[2*i1] = float(see_columns[i1].split("-")[0])
        plt_spec_wl[2*i1+1] = float(see_columns[i1].split("-")[1])
        
        plt_see_spec[2*i1] = see_spec.iloc[i1] * ymult_see
        plt_see_spec[2*i1+1] = see_spec.iloc[i1]* ymult_see
        
        plt_eve_spec[2*i1] = eve_spec.iloc[i1] * ymult_eve
        plt_eve_spec[2*i1+1] = eve_spec.iloc[i1]* ymult_eve
        
        plt_f10_spec[2*i1] = f10_sb_df.iloc[i1]
        plt_f10_spec[2*i1+1] = f10_sb_df.iloc[i1]
        
    fig, ax1 = plt.subplots()
    
    ax1.set_title("Stan-Band Spectrum  " + str(str_date))

    ax1.plot(plt_spec_wl,plt_see_spec,color='blue', label = "SEE Spectrum")
    ax1.plot(plt_spec_wl,plt_eve_spec,color='green', label = "EVE Spectrum")
    ax1.plot(plt_spec_wl,plt_f10_spec,color='red', label = "WAM F10 Spec")

    ax1.set_ylim(1e8,1e12) 
    ax1.set_xlim(60,130)
    ax1.set_yscale('log')
    ax1.legend(loc = 'upper left')
    
if plot_ts:
    
    sb_to_plot = 4
    
    ymin1 = -5e8
    ymax1 = 1.5e9
    
    ymin2 = 0
    ymax2 = 5
    
    ymult_eve = 1. 
    ymult_see = 1.   
    ymult_f10 = 1.
    
    str_date = dt.datetime(2010,8,1)
    end_date = dt.datetime(2014,1,1)
    
    see_col = see_sb_df.columns
    eve_col = eve_sb_df.columns
    

    eve_col_to_plot = eve_col[sb_to_plot]
    see_col_to_plot = see_col[sb_to_plot]
    f10_col_to_plot = f10_sb_df.columns[sb_to_plot]
    
    print("Plotting ", see_col_to_plot, eve_col_to_plot, f10_col_to_plot)
    
    eve_ts = eve_sb_df[eve_col_to_plot].loc[(eve_sb_df.index >= str_date)
                         & (eve_sb_df.index < end_date)] * ymult_eve
    see_ts = see_sb_df[see_col_to_plot].loc[(see_sb_df.index >= str_date)
                         & (see_sb_df.index < end_date)] * ymult_see
    f10_ts = f10_sb_df[f10_col_to_plot].loc[(f10_sb_df.index >= str_date)
                         & (f10_sb_df.index < end_date)] * ymult_f10
    
    see_ts_df = pd.DataFrame(see_ts)
    see_ts_df.rename(columns={see_ts_df.columns[0]:see_ts_df.columns[0]+"_see"},inplace = True)
    
    eve_ts_df = pd.DataFrame(eve_ts)
    eve_ts_df.rename(columns={eve_ts_df.columns[0]:eve_ts_df.columns[0]+"_eve"},inplace = True)
    
    f10_ts_df = pd.DataFrame(f10_ts)
    f10_ts_df.rename(columns={f10_ts_df.columns[0]:f10_ts_df.columns[0]+"_f10"},inplace = True)
    
    both_df = see_ts_df.join(eve_ts_df)
    both_df = both_df.join(f10_ts_df)
    both_df["ratio1"] = both_df[both_df.columns[0]]/both_df[both_df.columns[1]]
    both_df["ratio2"] = both_df[both_df.columns[0]]/both_df[both_df.columns[2]]
    
    
    fig, ax1 = plt.subplots()
    ax1.plot(see_ts,color = 'green', label = 'SEE Time Series')   
    ax1.plot(eve_ts, color = 'blue', label = 'EVE Time Series')

    ax1.plot(f10_ts,color = 'red', label = 'F10 Time Series')
    
    ax1.set_title("Stan-Band Channel " + see_col_to_plot)
    

    
    
    ax1.set_ylim(ymin1,ymax1) 
    
    ax2 = ax1.twinx()
        
       
    ax2.plot(both_df["ratio1"],label = "Ratio SEE/EVE", color = "black",lw = 1 )
    ax2.plot(both_df["ratio2"],label = "Ratio SEE/F10", color = "grey",lw = 1 )
    # ax2.axhline(1, color = 'k', lw = .5)
    # ax2.set_xlim(xmin,xmax)

    ax2.set_ylim(ymin2,ymax2) 
    
    ax1.legend(loc = "upper left")
    ax2.legend(loc = "upper right")
    

    
    plt.show()
    
    
stop()


# see_speca = see_df.iloc[2939:2953].mean(axis = 0)

# see_ts = see_df.iloc[10:15].sum(axis=0)

# npts = len(see_df.columns)
# see_spec = np.zeros(npts)
# see_wl = np.zeros(npts)
# for i1 in range (npts):
#     see_spec[i1] = see_speca.iloc[i1]
#     t_head = see_df.columns[i1]
#     ut_head = untuple(t_head) 
#     see_wl[i1] = [float(i) for i in re.findall(r'[\d]*[.][\d]+',ut_head)][0]  #Extract number from tuple

# see_df.columns = see_wl
# # see_df.rename(columns={see_wl},inplace = True)

# #  Convert to Photo ns

# # Convert to Photons

# # c = 2.998e8    # m/s Speed of light
# # h = 6.63e-34  #J.s Planks Constant
# #   E = hc/wl  =  i x wl x 5.05e15 * 1e-4 cm2/m2

# mf = 5.05e11

# for i1 in range (len(see_df.columns)):
#     see_df[see_df.columns[i1]] = see_df[see_df.columns[i1]] * see_df.columns[i1] * mf /1.e4

# # see_sb

# stop()



# for i1 in range(npts):
#     see_spec[i1] =  see_spec[i1] *  see_wl[i1] * mf /1.e4

# see_cols = ['See_Spec']
# see_spec_df = pd.DataFrame(data = see_spec[:], index = see_wl[:], columns = see_cols)
# see_spec_df.index.name = 'Wavelength'

# swllx = 30
# swlhx = 35

# cols = see_df.columns
# sel_cols = []
# for x in cols:
#     if x >= swllx and x < swlhx:
#         sel_cols.append(x)
        
# see_sum = see_df[sel_cols[0]].copy()


# for i1 in range (1, len(sel_cols)):
#     icol = sel_cols[i1]
#     see_sum = see_sum.iloc[0] + see_df[icol]
# see_sum = see_sum/len(see_cols)
    
# see_sum2 = pd.DataFrame(see_sum[see_sum>0])
# col_lab1 = str(swllx)+"-"+str(swlhx)
# see_sum2.columns = [col_lab1]


# # stop()
# #Get EVE Data


# eve_df = pd.read_csv(ipath+ifile_eve)
# eve_df['Datetime'] = pd.to_datetime(eve_df['Datetime'])
# eve_df.set_index('Datetime', inplace = True)

# stop()

# eve_speca = eve_df.iloc[100]


# npts = 100
# eve_spec = np.zeros(100)
# eve_wl = np.zeros(100)

# for i1 in range (npts):
#     eve_spec[i1] = eve_speca.iloc[i1]
#     eve_wl[i1] = 6.3 + i1

# # Convert to Photons

# for i1 in range(npts):
#     eve_spec[i1] =  eve_speca.iloc[i1] *  eve_wl[i1] * mf /1.e4
    
    
# eve_cols = ['EVE_Spec']
# eve_spec_df = pd.DataFrame(data = eve_spec[:], index = eve_wl[:], columns = eve_cols)
# eve_spec_df.index.name = 'Wavelength' 

# #Get EVE High_Res 

# eve_hr_file = 'SDO_EVE_spectra_2010-2014_V8.dat'

# eve_hr_df = pd.read_csv(ipath + eve_hr_file)  
# eve_hr_df.set_index('Datetime', inplace = True)
# eve_hr_df.index = pd.to_datetime(eve_hr_df.index)

# num_cols = len(eve_hr_df.columns)
# temp1 =  np.zeros(num_cols)
# for i1 in range (num_cols):temp1[i1] = float(eve_hr_df.columns[i1])
# eve_hr_df.columns = temp1

# wllx = 30
# wlhx = 35

# cols = eve_hr_df.columns
# sel_cols = []
# for x in cols:
#     if x >= wllx and x < wlhx:
#         sel_cols.append(x)
        
# eve_sum = eve_hr_df[sel_cols[0]].copy()


# for i1 in range (1, len(sel_cols)):
#     icol = sel_cols[i1]
#     eve_sum = eve_sum.iloc[0] + eve_hr_df[icol]
# eve_sum - eve_sum/len(sel_cols)
   
# eve_sum2 = pd.DataFrame(eve_sum[eve_sum>0])/5.
# col_lab1 = str(wllx)+"-"+str(wlhx)
# eve_sum2.columns = [col_lab1]

# #  Add another column to sum

# wlly = 20
# wlhy = 25

# sel_cols = []
# for x in cols:
#     if x >= wlly and x < wlhy:
#         sel_cols.append(x)
        
# eve_sum = eve_hr_df[sel_cols[0]].copy()


# for i1 in range (1, len(sel_cols)):
#     icol = sel_cols[i1]
#     eve_sum = eve_sum.iloc[0] + eve_hr_df[icol]
    
# eve_sum3 = pd.DataFrame(eve_sum[eve_sum>0])
# col_lab2 = str(wlly)+"-"+str(wlhy)
# eve_sum3.columns = [col_lab2]

# eve_sum_df = pd.concat([eve_sum2, eve_sum3], axis=1)

# c1 = eve_sum_df.columns


# # plt.plot(eve_sum_df[c1[0]], eve_sum_df[c1[1]], "o")
# # plt.xlabel(str(wllx)+'-'+str(wlhx)+" nm")
# # plt.ylabel(str(wlly)+'-'+str(wlhy)+" nm")
# # plt.show

# # eve_ts = eve_hr_df.loc[sel_cols].sum(axis=1)


# # eve_hr_spec = eve_hr_df.loc['2010-08-08']
# # eve_hr_spec_df = pd.DataFrame(data = eve_hr_spec[:], index = eve_hr_spec.index)
# # eve_hr_spec_df.rename(['2010-08-08', 'EVE_HR_Spec'])
# # eve_hr_spec_df.index.names = ['Wavelength']


# fig, ax1 = plt.subplots()



# ax1.set_title("EVE Time Series")
# # ewl = 30
# # ax1.plot(ewl * mf /1.e4 * see_df[see_df.columns[ewl]][see_df[see_df.columns[ewl]]>0], color = 'red', label = "SEE " + see_df.columns[ewl])
# # ax1.set_ylim(3.6e11,3.7e11)
# # ax1.plot(eve_sum_df[c1[0]], color = 'green', label = col_lab1) #, label = ("EVE "+str(wllx)+"-"+str(wlhx)+" nm"))
# ax1.plot(eve_sum_df[c1[0]],color='red', label = "EVE "+col_lab1)
# # ax1.plot(see_sum2, color = 'green', label = "SEE "+see_sum2.columns[0])
# # ax1 = plt.plot(pl_x,pl_y5,label = "EVE Hi Res StanBands")

# # ax1.set_yscale("log")
# # ax1.set_xlim(90,120)
# # ax1.set_ylim(1e4,1e12)
# # ax1.set_xlabel('Wavelength (nm)')
# ax1.set_ylabel('Flux (phot/cm2)')

# ax2 = ax1.twinx()

# # ax2.plot(eve_sum_df[c1[1]], color = 'green', label = "EVE "+col_lab2)
# ax2.plot(see_sum2, color = 'green', label = "SEE "+see_sum2.columns[0])
# # ax2.set_ylim(3.6505e11,3.654e11)
# # ax2.plot(eve_sum_df[c1[1]],color='red', label = col_lab2)
# # ax2.plot(26.5 * mf /1.e4 * see_df[see_df.columns[28]][see_df[see_df.columns[28]]>0], color = 'red', label = "SEE" + see_df.columns[26])
# # ax2.set_ylim(3e8,15e8)
# # ax2.plot(pl_ratios[0,:],pl_ratios[4,:],label = "Ratio EVE/NRL",color = "g")
# # ax2.plot(pl_ratios[0,:],pl_ratios[5,:],label = "Ratio SEE/NRL",color = "b")
# # ax2.plot(pl_ratios[0,:],pl_ratios[6,:],label = "Ratio SEE/EVE",color = "r")
# # ax2.set_ylabel('Ratio')
# # ax2.set_ylim(0.,5.)

# # plt.title("F10 Band = " + cols[i2] +   "    SEE Band = " + sb_col_names[i2])
# ax1.legend(loc = 'upper left')
# ax2.legend(loc = 'upper right')

# sdate = dt.datetime(year=2012,month=1,day=1)
# edate = dt.datetime(year=2013,month=1,day=1)

# # ax1.set_xlim(sdate, edate)


# save_plot = False
# # save_plot = True
# if save_plot:

#     ofile = "EVE_Hi_Res_Issues_6.jpg"
#     if save_plot:  plt.savefig(opath+ofile)
    
#     plt.show()
    
#     input("hit return to continue")
#     ofile = "EVE_Hi_Res_Ratio_6"
    
#     plt.plot(eve_sum_df[c1[0]]/eve_sum_df[c1[1]])
    
#     plt.plot()
#     if save_plot: plt.savefig(opath+ofile)

# plt.show()
