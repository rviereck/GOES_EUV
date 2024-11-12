# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 07:29:57 2022

@author: rodney.viereck
"""
# read_EVE_data


import astropy.io.fits as fits
import pandas as pd
import numpy as np

from datetime import datetime as dt
from datetime import timedelta as td

import requests
from bs4 import BeautifulSoup

save_file = True

iyear = '2019'
url_path = "https://lasp.colorado.edu/eve/data_access/eve_data/products/level4/"+iyear+"/"

opath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/SDO_EVE/"

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

result = requests.get(url_path)

soup = BeautifulSoup(result.text, 'html.parser')
fitsfiles = soup.find_all('a[href*=".fit"]')

filenames = []
for link in soup.select('a[href*=".fit"]'):
    filenames.append(link["href"])
    
numfiles = len(filenames)
# numfiles = 3

for i2 in range(numfiles):
    ifile = filenames[i2]
    print("Reading ",i2,ifile)
    
    # Parse year and DOY from filename
    yr = int(ifile[7:11])
    doy = int(ifile[11:14]) -1
    
    #  Read FITS file
    fdata =  fits.open(url_path + ifile)
    spec1 = fdata[1].data[0]
    fdata.close()
    
    #Extract Variables
    sod = spec1[0]  #Seconds of Day
    wavl = spec1[1].astype(float)  # Convert to float
    spec = spec1[2].astype(float)  # Convert to float
    
    moy = (doy * 1440.) + (sod / 60.) + 0.5  #Time of Day in Minutes
    
    #Convert minutes of day to DateTime array
    date_time = []
    for i1 in range (len(sod)):
        date_time.append(dt(yr,1,1) + td(minutes = float(moy[i1])))
        
    short_eve_df = pd.DataFrame(spec).transpose()  #Convert array to DataFrame
    
    #Create Column Names
    for i1 in range(len(wavl)):wavl[i1] = float(int(100 * wavl[i1]))/100.  #Truncate
    short_eve_df = short_eve_df.set_axis(wavl, axis = 1)  #Add Column Names
    
    # Create Date Index    
    short_eve_df.insert(0,'Datetime',date_time, True)
    short_eve_df = short_eve_df.set_index('Datetime')
    
    if i2 == 0:
        eve_df = short_eve_df
    else:
        eve_df = pd.concat([eve_df, short_eve_df])
        
        
        
        

# Create Stan Bands

print("Creating Stand Bands")

num_bands = 37

# Create first column of new Stan Band Dataframe from the XRS channels

wl_eve = pd.to_numeric(eve_df.columns)

wll = Stan_Bands[0,0]
wlh = Stan_Bands[0,1]
col_head = str(wll)+"-"+str(wlh)


eve_sb_df = pd.DataFrame(eve_df[eve_df.columns[(wl_eve>wll)&(wl_eve<=wlh)]].sum(axis=1))
eve_sb_df.rename(columns = {eve_sb_df.columns[0]:col_head},inplace = True)

wll = Stan_Bands[1,0]
wlh = Stan_Bands[1,1]
col_head = str(wll)+"-"+str(wlh)



print ("Fill In Rest of the Bands")

# wl_eve = pd.to_numeric(eve_df.columns)

for i1 in range(1,num_bands):
    wll = Stan_Bands[i1,0]
    wlh = Stan_Bands[i1,1]
    col_head = str(wll)+"-"+str(wlh)

    print("Band ", i1, col_head)
    if (i1 == 11 or i1 == 13 or i1 == 16):col_head = col_head + "_A"
    if (i1 == 12 or i1 == 14 or i1 == 17):col_head = col_head + "_B"
    if (i1 == 15 or i1 == 18):col_head = col_head + "_C"
    eve_sb_df[col_head] = ymult[i1] * eve_df[eve_df.columns[(wl_eve>wll)&(wl_eve<=wlh)]].sum(axis=1)
    
        
#Save to File

if save_file:
            
    ofile = "EVE_L4_SB_"+iyear+".dat"
    
    print("Write to file ", opath + ofile)
    
    eve_sb_df.to_csv(opath + ofile,float_format='%2.4e')
