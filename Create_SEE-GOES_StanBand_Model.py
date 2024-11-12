# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 07:29:57 2022

Combines annual TIMED-SEE HDF5 with MgII.

@author: rodney.viereck
"""
# read_EVE_data

import pandas as pd
# import netCDF4 as nc
from datetime import datetime as dt
from datetime import timedelta as tdelta
import matplotlib.pyplot as plt
import numpy as np
import array
import lmfit
import scipy

write_file = True
plots = False

# year = "2010"


# ipath = "C:/Users/rodney.viereck/Documents/Python/EUV/TIMED_SEE/input/"
ipath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/stan_bands/"
ifile = "SEE_GOES_Mg_Stan_Bands_2017-2024.dat"

f10_path = "C:/Users/rodney.viereck/Documents/Python/EUV/input/WAM_F10/"
f10_sb_file = "WAM_F10_Stan_Bands_2010-2020.dat"


opath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/stan_bands/"
ofile = "GOES_StanBand_Coefficients_2.dat"
# Select Dates
start_date = dt(2018,6,1)
end_date = dt(2024,10,1)

# see_spec = see_df.iloc[100][0:150]


  # *Ready to process the data

#Stan_Bands

 # 0.1-0.4     0.4-0.8     0.8-1.8     1.8-3.2     3.2-7.0     7.0-15.5    15.5-22.4  
 # 22.4-29.0   29.0-32.0   32.0-54.0   54.0-65.0   65.0-79.8   65.0-79.8   79.7-91.3   
 # 79.7-91.3   79.7-91.3   91.3-97.5   91.4-97.5   91.5-97.5   97.5-98.7  98.7-102.7   
 # 103.-105.   105.-110.   110.-115.   115.-120.   120.-121.   121.-125.   125.-130.   
 # 130.-135.   135.-140.   140.-145.   145.-150.   150.-155.   155.-160.   160.-165.   
 # 165.-170.   170.-175.
 
Stan_Bands = np.array([[0.1,0.4],[0.4,0.8],[0.8,1.8],[1.8,3.2],[3.2,7.0],[7.0,15.5],[15.5,22.4],\
     [22.4,29.0],[29.0,32.0],[32.0,54.0],[54.0,65.0],[65.0,79.8],[65.0,79.8],[79.7,91.3],\
     [79.7,91.3],[79.7,91.3],[91.3,97.5],[91.4,97.5],[91.5,97.5],[97.5,98.7],[98.7,102.7],\
     [103.,105.],[105.,110.],[110.,115.],[115.,120.],[120.,121.],[121.,125.],[125.,130.],\
     [130.,135.],[135.,140.],[140.,145.],[145.,150.],[150.,155.],[155.,160.],[160.,165.],\
     [165.,170.],[170.,175.]])
 
# stan_bands = [.1,.4,.8,1.8,3.2,7,15.5,22.4,29,32,54,65,79.8,91.3,97.5,\
#               98.7,102.7,103,105,110,115,120,121,125,130,135,140,145,\
#                   150,155,160,165,170,175]
    
# stan_bands_apx = [1,2,3,7,16,22,29,32,54,65,80,91,98,99,102,103,105,110\
#                   ,115,121,122,125,130,135,140,145,150,155,160,165,170,175]
    
# mixed_band_ratios = [[0.56,0.44,0.0],[0.34, 0.53, 0.13],[0.18,0.48,0.34]]

# GOES_lines = np.array([25.5,28.5,30.5,117.5,121.5,133.5,140.5])
# GOES_driver_columns = [25,28,30,117,121,133,140,176,178]
    
goes_lines = np.array([25.6,28.4,30.4,117.5,121.6,133.5,140.5])
goes_cols = np.array(['xrs_short','xrs_long','irr_256', 'irr_284', 'irr_304', 'irr_1175', 'irr_1216',\
        'irr_1335', 'irr_1405', 'MgII_standard'])

# goes_cols = [" "]*len(goes_lines)

# for i1 in range (len(goes_lines)):
#     goes_cols[i1] = "GOES_"+str(goes_lines[i1])
    
#Read F10 SBs
f10_sb_df = pd.read_csv(f10_path + f10_sb_file)
f10_sb_df['Datetime'] = pd.to_datetime(f10_sb_df['Datetime'])
f10_sb_df.set_index('Datetime', inplace = True)
f10_cols = f10_sb_df.columns



f10_sb_df = f10_sb_df[(f10_sb_df.index > start_date) & (f10_sb_df.index <= end_date)]


# ***************************  Read File *********

print(ipath + ifile)

sb_df = pd.read_csv(ipath+ifile)
sb_df['Datetime'] = pd.to_datetime(sb_df['Datetime'])
sb_df.set_index('Datetime', inplace = True)

sb_df = sb_df[(sb_df.index >= start_date) & (sb_df.index < end_date)]

goes_mod_df = pd.DataFrame(sb_df[sb_df.columns[0]])
# goes_mod_df.set_index('Datetime', inplace = True)

# *********************************************************

#              Create GOES Proxy Model

#  *****************   Fit Data  **************************

#model drivers
x0 = sb_df[goes_cols[0]]
x1 = sb_df[goes_cols[1]]
x2 = sb_df[goes_cols[2]]
x3 = sb_df[goes_cols[3]]
x4 = sb_df[goes_cols[4]]
x5 = sb_df[goes_cols[5]]
x6 = sb_df[goes_cols[6]]
x7 = sb_df[goes_cols[7]]
x8 = sb_df[goes_cols[8]]
x9 = sb_df[goes_cols[9]]


rows = ['xrs_short','xrs_long','irr_25.5', 'irr_28.5', 'irr_30.5', 'irr_117.5', 'irr_121.5',\
        'irr_133.5', 'irr_140.5', 'mg_standard' ,'constant', 'slope', 'intcept','r_val',\
        'p_val', 'std_err']


#  Fitting model  ****
def residual(p,x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,c):
    v = p.valuesdict()
    model = v['a0']*x0 + v['a1']*x1 + v['a2']*x2 + v['a3']*x3 + v['a4']*x4\
        + v['a5']*x5 + v['a6']*x6 + v['a7']*x7 + v['a8']*x8 + v['a9']*x9 +  v['c']
    return (model - y)

results_df = pd.DataFrame(rows, columns = ['inputs'])
    
num_vals = len(sb_df.index)


#   Calculate coefficients

num_bands = len(Stan_Bands)
    
for iband in range (num_bands):
    print( "Fitting to " + sb_df.columns[iband])

    # str_band = str(bands[iband,0] + 0.5)
    

    # sb_df = sb_df[sb_df[sb_df.iloc[iband]] > 0]
    sb_df = sb_df.dropna()
    y = sb_df[sb_df.columns[iband]]
    
    if max(y) > 0:
    
        p = lmfit.Parameters()
        p.add_many(('a0',1.),('a1',1.),('a2',1.),('a3',1.),('a4',1.),('a5',1.),('a6',1.),('a7',1.),('a8',1.),('a9',1.),('c',1.))
    
        mi = lmfit.minimize(residual,p, args = (x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,y) , method='Leastsq' )
    
        # lmfit.printfuncs.report_fit(mi.params)
        
        aa0 = float(mi.params['a0'] )
        aa1 = float(mi.params['a1'])
        aa2 = float(mi.params['a2'])
        aa3 = float(mi.params['a3'])
        aa4 = float(mi.params['a4'])
        aa5 = float(mi.params['a5'])
        aa6 = float(mi.params['a6'])
        aa7 = float(mi.params['a7'])
        aa8 = float(mi.params['a8'])
        aa9 = float(mi.params['a9'])
        cc = float(mi.params['c'])
        
        
        model2 = aa0*x0 + aa1*x1 + aa2*x2 + aa3*x3 + aa4*x4 + aa5*x5 + aa6*x6 + aa7*x7 + aa8*x8 + aa9*x9 + cc
        
        slope, intercept, r_value, p_value, std_err, = scipy.stats.linregress(y, model2)
            #print (r_value,p_value, std_err)
            
        column = [aa0,aa1,aa2,aa3,aa4,aa5,aa6,aa7,aa8,aa9,cc,slope, intercept, r_value, p_value, std_err]

    else:
        column = [0]*16
        model2 = y
        
    results_df[sb_df.columns[iband]] = column
    
    goes_mod_df[sb_df.columns[iband]] = model2
    
    if plots:
        

        
        
        
        fig, ax1 = plt.subplots()

        # ax2 = ax1.twinx()

        ax1.set_title(sb_df.columns[iband]+" nm")
        
        print('Plotting ', iband, sb_df.columns[iband])
        ax1.plot(sb_df[sb_df.columns[iband]],label = "SEE Data", color = "blue")
        ax1.plot(model2, label = 'Model', color = "red")
        # ax1.plot((f10_sb_df[f10_cols[iband]]), color = "blue", label = "WAM F10 SB " + f10_cols[iband])
        
        
        # ax2 = ax1.twinx()
        # ax2.plot((1e4*f10_sb_df[f10_cols[iband]]), color = "black", label = "F10_SB " + f10_cols[iband])

        plt.legend()
        plt.show() 
        
                
        input("Press Enter to continue...")
        
        fig, ax2 = plt.subplots()

        # ax2 = ax1.twinx()

        ax2.set_title(sb_df.columns[iband]+" nm")
        
        print('Scatter Plotting ', iband, sb_df.columns[iband])
        
        xmin = model2.min()
        xmax = model2.max()
        plinex = ([xmin,xmax])
        pliney = ([xmin,xmax])
        
        
        ax2.scatter(sb_df[sb_df.columns[iband]],model2, color = "red", s = 0.2)
        ax2.plot(plinex,pliney,color = 'black', linewidth = .3)
        
        ax2.set_xlabel("SEE Stan-Band")
        ax2.set_ylabel("GOES-Driven Stan-Band")
        plt.show() 

        input("Press Enter to continue...")

if write_file:
    print('Saving GOES Stan_Band coefficients to ', opath +ofile)
    results_df.set_index('inputs', inplace = True)
    # results_df[results_df < 1e-10] = 0
    results_df.to_csv(opath +ofile, float_format='%.4e')
    


